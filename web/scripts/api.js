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
            yield fetch('/graphs', {
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
            });
        });
    }
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
    fetchNodes() {
        return __awaiter(this, void 0, void 0, function* () {
            let data = yield fetch('/nodes')
                .then(response => {
                if (response.ok) {
                    return response.json();
                }
                else if (response.status === 404) {
                    return Promise.reject('error 404');
                }
            }, null);
            return data;
        });
    }
}
