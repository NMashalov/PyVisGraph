var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __classPrivateFieldGet = (this && this.__classPrivateFieldGet) || function (receiver, state, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state === "function" ? receiver !== state || !f : !state.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state.get(receiver);
};
var _pydanticGraphImpl_instances, _pydanticGraphImpl_load_graph, _pydanticGraphImpl_set_download_button;
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
        if (model.properties) {
            this.properties = {};
            for (const [name, prop] of Object.entries(model.properties)) {
                const def_value = prop.default_value || '0';
                this.properties[name] = def_value;
                this.addWidget("text", name, def_value, { property: name });
            }
        }
        ;
        this.size = this.computeSize();
    }
    ;
    // add helper on hover
    // it will written multiline as usual
    if (model.helper || model.properties) {
        CustomNode.prototype.onDrawBackground = function (ctx) {
            if (this.mouseOver) {
                ctx.fillStyle = "#AAA";
                let diff = 14;
                // display header if only we have it
                if (model.helper) {
                    var lines = model.helper.split('\n');
                    for (var i = 0; i < lines.length; i++) {
                        ctx.fillText(lines[i], 0, this.size[1] + diff);
                        diff += 14;
                    }
                }
                // display properties only if them have description
                for (const [name, prop] of Object.entries(model.properties)) {
                    if (prop.description) {
                        ctx.fillText(`@${name}: ${prop.description}`, 0, this.size[1] + diff);
                        diff += 14;
                    }
                }
            }
        };
    }
    CustomNode.title = model.name;
    LiteGraph.registerNodeType(`custom/${CustomNode.title}`, CustomNode);
}
;
;
class pydanticGraphImpl {
    constructor(api) {
        _pydanticGraphImpl_instances.add(this);
        this.api = api;
        this.graph = new LGraph();
    }
    registerNodes() {
        return __awaiter(this, void 0, void 0, function* () {
            // Load node definitions from the backend
            yield this.api.fetchNodes()
                .then(defs => defs === null || defs === void 0 ? void 0 : defs.forEach((x, i) => modelToNode(x), null)).catch(error => console.log('error is', error));
        });
    }
    ;
    setup() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.registerNodes();
            var canvas = new LGraphCanvas("#mycanvas", this.graph);
            canvas.onDropItem = function (e) {
                var that = this;
                for (var i = 0; i < e.dataTransfer.files.length; ++i) {
                    var file = e.dataTransfer.files[i];
                    var ext = LGraphCanvas.getFileExtension(file.name);
                    // uploading graph
                    if (ext == "json") {
                        var reader = new FileReader();
                        reader.onload = function (event) {
                            var data = JSON.parse(event.target.result);
                            that.graph.configure(data);
                        };
                    }
                    // uploading new nodes
                    else if (ext == "py") {
                        fetch('/parse_nodes', {
                            method: 'POST',
                            body: file
                        });
                    }
                    this.registerNodes();
                }
            };
            __classPrivateFieldGet(this, _pydanticGraphImpl_instances, "m", _pydanticGraphImpl_set_download_button).call(this);
            this.graph.start();
        });
    }
}
_pydanticGraphImpl_instances = new WeakSet(), _pydanticGraphImpl_load_graph = function _pydanticGraphImpl_load_graph() {
}, _pydanticGraphImpl_set_download_button = function _pydanticGraphImpl_set_download_button() {
    var header = document.getElementById("InstrumentHeader");
    var elem = document.createElement("span");
    elem.id = "InstrumentPanel";
    elem.className = "selector";
    elem.innerHTML = ("<button class='btn' id='download'>Download</button>\
			<button class='btn' id='validate'>Validate</button>");
    header.appendChild(elem);
    const graph = this.graph;
    const api = this.api;
    elem.querySelector("#download").addEventListener("click", function () {
        return __awaiter(this, void 0, void 0, function* () {
            var data = JSON.stringify(graph.serialize());
            yield api.send_graph_json(data);
        });
    });
    elem.querySelector("#validate").addEventListener("click", function () {
        return __awaiter(this, void 0, void 0, function* () {
            var data = JSON.stringify(graph.serialize());
            yield api.send_graph_json(data);
            alert('Wrong Graph!');
        });
    });
};
;
export const app = new pydanticGraphImpl(new Api());
