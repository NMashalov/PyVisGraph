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
class pydanticGraph {
    constructor(api) {
        this.api = api;
    }
    registerNodes() {
        return __awaiter(this, void 0, void 0, function* () {
            const app = this;
            // Load node definitions from the backend
            yield this.api.fetchNodes()
                .then(defs => defs.forEach((x, i) => modelToNode(x)));
        });
    }
    ;
    setup() {
        return __awaiter(this, void 0, void 0, function* () {
            this.graph = new LGraph();
            yield this.registerNodes();
            var canvas = new LGraphCanvas("#mycanvas", this.graph);
            this.graph.start();
        });
    }
}
export const app = new pydanticGraph(new Api());
