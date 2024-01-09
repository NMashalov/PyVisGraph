var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { Api } from './api.js';
// var LiteGraph = global.LiteGraph;
export function modelToNode(model) {
    function CustomNode() {
        // register input
        if (model.input) {
            model.input.forEach((x, i) => this.addInput(x.name, x.type));
        }
        ;
        // register output
        if (model.output) {
            model.output.forEach((x, i) => this.addOutput(x.name, x.type));
        }
        ;
        // register name
        this.properties = Object.assign({}, model.properties);
        if (model.properties) {
            model.properties.forEach((x, i) => this.addWidget("text", x.name, "", { property: x.name }));
        }
        ;
    }
    ;
    CustomNode.title = model.name;
    LiteGraph.registerNodeType(`custom/${CustomNode.title}`, CustomNode);
}
class pydanticGraphImpl {
    constructor(api) {
        this.api = api;
        this.graph = new LGraph();
        console.log(this.graph.serialize());
    }
    registerNodes() {
        return __awaiter(this, void 0, void 0, function* () {
            // Load node definitions from the backend
            yield this.api.fetchNodes()
                .then(defs => defs.forEach((x, i) => modelToNode(x)));
        });
    }
    ;
    set_download_button() {
        var header = document.getElementById("InstrumentHeader");
        var elem = document.createElement("span");
        elem.id = "InstrumentPanel";
        elem.className = "selector";
        elem.innerHTML = "<button class='btn' id='download'>Download</button>";
        header.appendChild(elem);
        const graph = this.graph;
        elem.querySelector("#download").addEventListener("click", function () {
            var data = JSON.stringify(graph.serialize());
            var file = new Blob([data]);
            var url = URL.createObjectURL(file);
            var element = document.createElement("a");
            element.setAttribute('href', url);
            element.setAttribute('download', "graph.JSON");
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
            setTimeout(function () { URL.revokeObjectURL(url); }, 1000 * 60); //wait one minute to revoke url	
        });
    }
    setup() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.registerNodes();
            var canvas = new LGraphCanvas("#mycanvas", this.graph);
            this.set_download_button();
            this.graph.start();
        });
    }
}
export const app = new pydanticGraphImpl(new Api());
