import {Api, ModelSchema} from './api.js'

declare var LiteGraph, LGraph, LGraphCanvas;

// var LiteGraph = global.LiteGraph;


export function modelToNode(model : ModelSchema)
{
	function CustomNode(){
		// register input
		if (model.input){
			model.input.forEach((x,i) => this.addInput(x.name,x.type));
		};
		// register output
		if (model.output){
			model.output.forEach((x,i) => this.addOutput(x.name,x.type));
		};
		// register name
		this.properties = {
			...model.properties
		};

		if (model.properties){
			model.properties.forEach((x,i) => this.addWidget("text",x.name,"", { property: x.name}));
		};	
	};

	CustomNode.title = model.name;

	LiteGraph.registerNodeType(`custom/${CustomNode.title}`,CustomNode)
}


class pydanticGraph{
	api: Api;
	graph: any;


    constructor(api: Api) {
		this.api = api;
	}


    async registerNodes() {
        const app = this;
        // Load node definitions from the backend
        await this.api.fetchNodes()
			.then(defs => defs.forEach(
				(x,i) => modelToNode(x))
			);
    };

    async setup(){
        this.graph = new LGraph();
        await this.registerNodes();

        var canvas = new LGraphCanvas("#mycanvas", this.graph);

        this.graph.start()
    }
}

export const app = new pydanticGraph(new Api()); 

