Vue.prototype.$http = axios;

let app = new Vue({
    el: '#main-app',
    data: {
        /* Данные от пользователя. Сортировка и поиск записи */
        sortParam: {column: '', order: 1},  // 1 - ASC, -1 - DSC
        searchQuery: '',

        /* Данные о столбцах приходят от сервера. Поле "Columns" */
        columnsHeaders: [],
        // columnsHeaders: [
        //     {'name': 'user_team_alias',
        //      'displayName': 'Позывной',
        //      'search': 1,
        //      'sort': 1,
        //      'width': ''
        // }],

        /* Данные приходят от сервера. Поле "Data" */
        // columnsData: [],
        columnsDataROW: [],
        // {
        //     "user_status": 0,
        //     "user_comment": null,
        //     "user_pk": 25,
        //     "user_name": "\u0421\u0430\u0432\u0435\u043d\u043a\u043e \u0410\u043d\u0442\u043e\u043d\u0438\u0439"
        //     "user_team_alias": "\u0421\u0430\u0432\u0435\u043d\u043a\u043e \u0410\u043d\u0442\u043e\u043d\u0438\u0439"
        // },
        dataURL: '',
    },
    created: function () {
        this.getDataURL();
        this.fetchData();
    },

    computed: {
        columnsData: function () {
            let tmpData = this.columnsDataROW;
            let self = this;
            let filter = self.searchQuery.toLowerCase();
            let sort = self.sortParam;

            /* Фильтрация для заданных полей (унифицировать) */
            if (filter) {
                return tmpData.filter(function (row) {

                    // let byName = row.user_name.indexOf(self.searchQuery) !== -1;
                    // let byAlias = row.user_team_alias.indexOf(self.searchQuery) !== -1;
                    // return byName || byAlias;

                    let tmp = []
                    for (let col of self.searchColumns){
                        tmp.push(row[col].toLowerCase().indexOf(filter) !== -1);
                    }
                    return tmp.some(elem => elem);
                });

            /* Сортировка. Действует по только для одного поля */
            } else if (sort.column) {
                return tmpData.sort(function (d1, d2) {
                    let sort_field = sort.column.name;
                    if (sort.order > 0) {
                        return ((d1[sort_field] || '').toLowerCase() > (d2[sort_field] || '').toLowerCase()) ? 1 : -1;
                    } else {
                        return ((d1[sort_field] || '').toLowerCase() < (d2[sort_field] || '').toLowerCase()) ? 1 : -1;
                    }
                });
            } else {
                return tmpData;
            }
        },

        /* Имена столбцов используемых в поиске */
        searchColumns: function (){
            let self = this;
            let columns = [];
            for (let col of self.columnsHeaders){
                if (col.search === 1) {
                    columns.push(col.name);
                }
            }
            return columns;
        },

        /* Имена столбцов используемых в поиске */

        sortColumns: function (){
            let self = this;
            let columns = [];
            for (let col of self.columnsHeaders){
                if (col.sort === 1) {
                    columns.push(col.name);
                }
            }
            return columns;
        }

    },

    methods: {
        /* Получение данных с сервера */
        fetchData: function () {
            let self = this;
            this.$http.get(self.dataURL)
                .then(function (response) {
                    // self.columnsData = response.data.Data;
                    self.columnsDataROW = response.data.Data;
                    self.columnsHeaders = response.data.Columns;
                });
        },

        /* Получение ссылки из шаблона на данные */
        getDataURL: function (){
            let self = this;

            // const event_reg = JSON.parse(document.getElementById('events_register_url').textContent);
            console.log(document.getElementById('dataURL'))
            self.dataURL = JSON.parse(document.getElementById('dataURL').textContent);
            console.log(self.dataURL);
        }
    }
});
