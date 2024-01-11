var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
let API_URL = '';
let API_PORT = "8000";
let NODE_PATH = 'nodes';
export class Api {
    constructor() {
        this.url = `${API_URL}:${API_PORT}/${NODE_PATH}`;
        console.log(this.url);
    }
    send_graph_json(graph_json) {
        return __awaiter(this, void 0, void 0, function* () {
            return yield fetch('/graphs', {
                method: 'POST', // или 'PUT'
                body: JSON.stringify({
                    body: graph_json, // данные могут быть 'строкой' или {объектом}!
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }), // данные могут быть 'строкой' или {объектом}!
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then((response) => __awaiter(this, void 0, void 0, function* () {
                if (response.ok) {
                    alert('ok');
                    return response.json();
                }
                else if (response.status === 404) {
                    return Promise.reject('error 404');
                }
                else if (response.status === 418) {
                    let j = JSON.parse(yield response.json());
                    let alert_msg = '';
                    j.forEach((el, i) => {
                        alert_msg += `Error. Field ${el['loc']} has received msg ${el['msg']}\n`;
                    });
                    alert(alert_msg);
                }
                else if (response.status === 421) {
                    let j = yield response.json();
                    alert(j);
                }
                else if (response.status === 500) {
                    alert('500 Server Error');
                }
            }), null);
        });
    }
    ;
    parseNodesFromFile(file) {
        return __awaiter(this, void 0, void 0, function* () {
            const formData = new FormData();
            formData.append("file", file, file.name);
            return yield fetch('/parse_nodes', {
                method: 'POST',
                body: formData
            }).then(response => {
                if (response.ok) {
                    return response.json();
                }
                else if (response.status === 404) {
                    return Promise.reject('error 404');
                }
            }, null);
        });
    }
    fetchLocalNodes() {
        return __awaiter(this, void 0, void 0, function* () {
            let data = yield fetch('/local_nodes')
                .then((response) => __awaiter(this, void 0, void 0, function* () {
                if (response.ok) {
                    return response.json();
                }
                else if (response.status === 404) {
                    return Promise.reject('error 404');
                }
            }), null);
            return data;
        });
    }
    fetchDagSettings() {
        return __awaiter(this, void 0, void 0, function* () {
            let data = yield fetch('/dag_fields')
                .then((response) => __awaiter(this, void 0, void 0, function* () {
                if (response.ok) {
                    return response.json();
                }
                else if (response.status === 404) {
                    return Promise.reject('error 404');
                }
            }), null);
            return data;
        });
    }
}
