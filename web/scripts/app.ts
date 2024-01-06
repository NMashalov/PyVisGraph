import {LGraph, LiteGraph} from './lib/litegraph.js'
import {
	Api,
	Property,
	Link,
	ModelSchema
} from './api.ts'




function modelToNode(model : ModelSchema)
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
		this.title = model.name;
		this.properties = {
			...model.properties
		};
	};

	return model.name,CustomNode;
}


export class pydanticGraph{
	api: Api;
	graph: any;


    constructor(api: Api) {
		this.api = api;
	}


    async registerNodes() {
        const app = this;
        // Load node definitions from the backend
        const defs = await this.api.fetchNodes();

		defs.forEach(
			(x,i) => LiteGraph.registerNodeType(modelToNode(x))
		)
        await this.registerNodesFromDefs(defs);
    }

    async setup(){
        this.graph = new LGraph();
        await this.registerNodes();

        var canvas = new LGraphCanvas("#mycanvas", graph);

        graph.start()
    }
}

