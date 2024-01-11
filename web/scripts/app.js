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
var _pydanticGraphImpl_instances, _pydanticGraphImpl_registerNodes, _pydanticGraphImpl_set_header;
import { Api } from './api.js';
// var LiteGraph = global.LiteGraph;
function modelToNode(model, name) {
    console.log(model);
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
        this.properties['hash'] = model.hash;
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
    LiteGraph.registerNodeType(`${name}/${CustomNode.title}`, CustomNode);
}
;
;
class pydanticGraphImpl {
    constructor(api) {
        _pydanticGraphImpl_instances.add(this);
        this.api = api;
        this.graph = new LGraph();
        this.dagName = 'Dummy';
    }
    ;
    setup() {
        return __awaiter(this, void 0, void 0, function* () {
            yield __classPrivateFieldGet(this, _pydanticGraphImpl_instances, "m", _pydanticGraphImpl_registerNodes).call(this, this.api.fetchLocalNodes());
            var canvas = new LGraphCanvas("#mycanvas", this.graph);
            const that = this;
            canvas.onDropItem = function (e) {
                return __awaiter(this, void 0, void 0, function* () {
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
                            console.log();
                            __classPrivateFieldGet(that, _pydanticGraphImpl_instances, "m", _pydanticGraphImpl_registerNodes).call(that, that.api.parseNodesFromFile(file));
                        }
                    }
                });
            };
            __classPrivateFieldGet(this, _pydanticGraphImpl_instances, "m", _pydanticGraphImpl_set_header).call(this);
            this.graph.start();
        });
    }
}
_pydanticGraphImpl_instances = new WeakSet(), _pydanticGraphImpl_registerNodes = function _pydanticGraphImpl_registerNodes(promise) {
    return __awaiter(this, void 0, void 0, function* () {
        // Load node definitions from the backend
        yield promise
            .then(modules => modules.forEach((module, _) => module.nodes.forEach((x, _) => modelToNode(x, module.module_name))), null).catch(error => console.log('error is', error));
    });
}, _pydanticGraphImpl_set_header = function _pydanticGraphImpl_set_header() {
    var header = document.getElementById("InstrumentHeader");
    var elem = document.createElement("span");
    elem.id = "InstrumentPanel";
    elem.className = "selector";
    elem.innerHTML = ("<button class='btn' id='download'>Download</button>\
			<button class='btn' id='validate'>Validate</button>\
			<input type='text' id='changeDagName' value='Enter Dag Name'>");
    header.appendChild(elem);
    elem.querySelector("#download").addEventListener("click", () => __awaiter(this, void 0, void 0, function* () {
        var data = {};
        data['graph'] = this.graph.serialize();
        data['dag_name'] = this.dagName;
        var response = yield this.api.send_graph_json(data);
        var file = new Blob([response]);
        var url = URL.createObjectURL(file);
        var element = document.createElement("a");
        element.setAttribute('href', url);
        element.setAttribute('download', "graph.yaml");
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }));
    elem.querySelector("#validate").addEventListener("click", () => __awaiter(this, void 0, void 0, function* () {
        var data = JSON.stringify(this.graph.serialize());
        yield this.api.send_graph_json(data);
        alert('Wrong Graph!');
    }));
    elem.querySelector("#changeDagName").addEventListener("change", (e) => {
        console.log(e.target.value);
        this.dagName = e.target.value;
    });
};
;
export const app = new pydanticGraphImpl(new Api());
