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
    fetchNodes() {
        return __awaiter(this, void 0, void 0, function* () {
            let data = yield fetch('/nodes')
                .then(response => response.json());
            return data;
        });
    }
}
