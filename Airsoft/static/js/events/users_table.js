Vue.prototype.$http = axios;

let app = new Vue({
    el: '#main-app',
    data: {
        /* Данные от пользователя. Сортировка и поиск записи */
        sortParam: {column: '', order: 1},  // 1 - ASC, -1 - DSC
        searchQuery: '',

        searchQuery: '',                    // Строка в поле для поиска
        selectedColumns: [],
        dataQuery: "",
        allowedSources: [],                 // TODO  api/allowlist

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
        // this.fetchConfig();
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

                    let tmp = []
                    for (let col of self.searchColumns){
                        tmp.push((row[col] || '').toLowerCase().indexOf(filter) !== -1);
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
        /* Составление запроса по выбранным полям */
        buildQuery: function () {
            let self = this;

            let columns = "&columns=["
            self.selectedColumns.forEach((item, index, array) => {
                columns += `"${item.name}",`
            });
            columns = columns.slice(0, -1)
            columns += "]"
            self.dataQuery += columns
        },

        buildTable: function (event) {
            let self = this;
            self.dataQuery = ''
            self.buildQuery()

            console.log(self.dataURL + '?target="MAIN_VALUES"' + self.dataQuery)

            this.$http.get(self.dataURL + '?target="MAIN_VALUES"' + self.dataQuery)
                .then(function (response) {
                    self.columnsDataROW = response.data;
                });
        },

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

        // fetchConfig: function () {
        //     let self = this;
        //     this.$http.get(self.configURL)
        //         .then(function (response) {
        //             console.log(response.data)
        //             // self.allowedSources = response.data // TODO right module
        //             // self.columnsDataROW = response.data.Data;
        //             self.columnsHeaders = response.data.Columns;
        //         });
        // },
        
        /* Получение ссылки из шаблона на данные */
        getDataURL: function (){
            let self = this;

            // const event_reg = JSON.parse(document.getElementById('events_register_url').textContent);
            self.dataURL = JSON.parse(document.getElementById('dataURL').textContent);
            console.log(self.dataURL);
                // + '?filter_patt=cancelTable';
            // self.configURL = "http://127.0.0.1:8000/api/allowlist"
            // self.dataURL = "http://127.0.0.1:8000/api/data"
            // console.log(self.configURL);
            // console.log(self.dataURL);

        },

        /* Отменить посещение для игрока */
        cancelVisit: function (user_row) {
            let self = this;
            let reg_cancelURL = JSON.parse(document.getElementById('reg_cancelURL').textContent) + `?reg_id=${user_row.user_event_pk}`;
            this.$http.get(reg_cancelURL)
                .then(function (response) {
                    if (response.data.stateside === 200){
                        if (user_row.user_status_code === 0){
                            user_row.visited = false;
                            user_row.user_status_code = 4;
                            user_row.user_status = 'Не явился';
                        } else {
                            user_row.visited = true;
                            user_row.user_status_code = 0;
                            user_row.user_status = 'Зарегистрировался';
                        }
                    } else {
                        console.log(response.data.stateside)
                        alert('Что-то пошло не так')
                    }
                });
        }
    }
});