from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from os.path import join as osjoin, exists
import json
from os import getcwd
import logging

"""
Получить список таблиц (разрешённых)
    для каждой таблицы список полей для отображения 

Получить данные для выбранной таблицы и полей
    фильтрация данных
    
"""
CONF_FILE = osjoin(getcwd(), f'api\\files\\tables.json')
logger = logging.getLogger(__name__)


class LoapOptionFilterParser:
    OPERATORS = {"contains": {"format": "({} like %({})s)", "extra_value": "%{}%"},
                 "notcontains": {"format": "(not {} like %({})s)", "extra_value": "%{}%"},
                 "startswith": {"format": "({} like %({})s)", "extra_value": "{}%"},
                 "endswith": {"format": "({} like %({})s)", "extra_value": "%{}"},
                 "=": {"format": "({}=%({})s)"},
                 "<>": {"format": "({}!=%({})s)"},
                 ">=": {"format": "({}>=%({})s)"},
                 "<": {"format": "({}<%({})s)"},
                 "<=": {"format": "({}<=%({})s)"},
                 ">": {"format": "({}>%({})s)"},
                 "and": {"format": "({} and {})"},
                 "or": {"format": "({} or {})"}}

    def __init__(self, original: list, pseudo=None):
        self.original = original
        self.pseudo = pseudo or {}
        self.data = {}
        self.counter = 0

    def parse_filter(self):
        self.result = "true"
        for _ in range(30):
            self.result = self.requrse_it(self.original.copy(), [])
            if self.result:
                return self.result, self.data
        return self.result, self.data

    def requrse_it(self, whatrecurse, position):
        reqursed = False
        for ind, i in enumerate(whatrecurse):
            if isinstance(i, list):
                reqursed = True
                self.requrse_it(i, position + [ind])
        if not reqursed:
            if position:
                here = self.original
                for i in position[:-1]:
                    here = here[i]
                if len(here[position[-1]]) == 3 and here[position[-1]][1] != "and" and here[position[-1]][1] != "or":
                    _format = LoapOptionFilterParser.OPERATORS.get(here[position[-1]][1], {}).get("format", "")
                    extra_value = LoapOptionFilterParser.OPERATORS.get(here[position[-1]][1], {}).get("extra_value",
                                                                                                       "")
                    self.counter += 1
                    if _format:
                        if here[position[-1]][-1] == "":
                            _format = '({} is Null)'.format(
                                self.pseudo.get(here[position[-1]][0], here[position[-1]][0]), self.counter)
                        else:
                            _format = _format.format(self.pseudo.get(here[position[-1]][0], here[position[-1]][0]),
                                                     self.counter)
                        if extra_value:
                            self.data[str(self.counter)] = extra_value.format(here[position[-1]][2])
                        else:
                            self.data[str(self.counter)] = here[position[-1]][2] if here[position[-1]][
                                                                                         2] != "" else 'Null'
                    else:
                        _format = "true"
                    here[position[-1]] = _format
                else:
                    here[position[-1]] = "(" + " ".join(here[position[-1]]) + ")"
            else:
                if len(self.original) == 3 and self.original[1] != "and" and self.original[1] != "or":
                    self.counter += 1
                    extra_value = LoapOptionFilterParser.OPERATORS.get(self.original[1], {}).get("extra_value")
                    if extra_value:
                        self.data[str(self.counter)] = extra_value.format(self.original[2])
                    else:
                        self.data[str(self.counter)] = self.original[2] if self.original[2] != '' else 'Null'
                    if self.original[2] == "" and self.original[1] == "=":
                        self.original = '({} is Null)'.format(self.pseudo.get(self.original[0], self.original[0]))
                    else:
                        self.original = LoapOptionFilterParser.OPERATORS.get(self.original[1], {}).get("format",
                                                                                                       "{} {}").format(
                            self.pseudo.get(self.original[0], self.original[0]), self.counter)
                elif len(self.original) == 2:
                    self.original = '{}={}'.format(self.original[0], repr(self.original[1]))
                else:
                    self.original = " ".join(self.original)
                return self.original


def check_allowed_col(input_col: list, table_name: str, tables_conf):
    """Исключить колонки, которые не разрешены для получения"""
    result = []
    for t in tables_conf:
        if t['name'] == table_name:
            result = [c["name"] for c in t['columns']]

    return list(set(result) & set(input_col))


def get_list(org: str):
    result = []
    try:
        result = json.loads(org)
    except Exception as err:
        pass
    finally:
        return result


def get_config(filepath=CONF_FILE):
    if exists(CONF_FILE):
        with open(CONF_FILE, encoding="utf_8_sig") as f:
            return json.load(f)
    return []


def dictFetchall(cursor):
    """Returns all rows from a cursor as a dict"""
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


class AllowList(APIView):
    def get(self, request):
        query_params = request.query_params
        target = query_params.get('object', None)
        tables_conf = get_config()

        if not tables_conf:
            Response("Error: config file not found", status=510)

        if target is not None and target != 'all':
            for t in tables_conf:
                if t.get('name', None) == target:
                    tables_conf = t
                    break
        return Response(tables_conf, status=200)


class WakeUp(APIView):
    # permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response("Ok", status=200)


# TODO UNused
class TestData(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute('''SELECT * FROM romario.D_ORG a Inner JOIN MAIN_VALUES b ON b.orgID=a.idORG''')
            data = dictFetchall(cursor)
        return Response({"answer": data})

# TODO Rewrite according team models 
class GetData(APIView):
    def get(self, request):
        """target its table name"""
        q_params = request.query_params
        columns = get_list(q_params.get('columns', None))
        DATA = {}

        target = get_list(q_params.get('target', None))
        if len(target) > 1:
            # TODO change this code
            tmp = "D_ORG Inner JOIN MAIN_VALUES ON MAIN_VALUES.orgID=D_ORG.idORG"
        target = target if type(target) is not list else target[0]


        WHERE = ""
        _filter = q_params.get('filter', default="")
        if _filter:
            _filter = json.loads(_filter)
            _filtered, DATA = LoapOptionFilterParser(_filter).parse_filter()
            WHERE = "WHERE " + _filtered
        tables_conf = get_config()
        response = []

        if not tables_conf:
            Response("Error: config file not found", status=510)

        with connection.cursor() as cursor:
            if columns is None:
                cursor.execute(f'''SELECT * FROM {target}''', DATA)
                response = dictFetchall(cursor)
            else:
                # columns = get_list(columns)
                columns = check_allowed_col(columns, target, tables_conf)
                query = 'SELECT {}, (SELECT count(valueval) FROM {}) row_count FROM {} {};'.format(', '.join(columns),
                                                                                                   target, target,
                                                                                                   WHERE)
                # cursor.execute(f'''SELECT {', '.join(columns)} FROM {target} {WHERE}''')
                cursor.execute(query, DATA)
                response = dictFetchall(cursor)
        return Response(response)

        #
        # if target is not None and target != 'all':
        #     for t in tables_conf:
        #         if t.get('name', None) == target:
        #             tables_conf = t
        #             break
        # return Response(tables_conf, status=200)
# filter=[["Host","=","181.215.183.196"],"or",["Host","=","141.98.119.232"]]
# http://127.0.0.1:8000/api/data/MAIN_VALUES/?columns=[valueval,value_measureval,d2ateval]&filter=[["valueval",">","2000"],"or",["value_measureval","=","twsdf"]]



# http://127.0.0.1:8000/api/data?target=%22MAIN_VALUES%22&columns=[%22valueval%22,%22value_measureval%22,%22d2ateval%22]&filter=[[%22valueval%22,%22%3E%22,%221991000%22],%22or%22,[%22value_measureval%22,%22=%22,%22twsdf%22]]
# http://127.0.0.1:8000/api/data/MAIN_VALUES/?columns=[%22valueval%22,%22value_measureval%22,%22d2ateval%22]&filter=[[%22valueval%22,%22%3E%22,%221991000%22],%22or%22,[%22value_measureval%22,%22=%22,%22twsdf%22]]
# http://127.0.0.1:8000/api/data/MAIN_VALUES/?columns=[valueval,value_measureval,d2ateval]&filter=[[id,%20eq,%2010]]
# http://127.0.0.1:8000/api/data/kek/
# http://127.0.0.1:8000/#


# SELECT * FROM romario.D_ORG a
# JOIN MAIN_VALUES b ON b.orgID=a.idORG;
