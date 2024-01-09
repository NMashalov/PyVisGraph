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
		
		if (model.properties){
			this.properties = {}
			
			for (const [name, prop] of Object.entries(model.properties)){
				const def_value = prop.default_value || '0'
				this.properties[name] = def_value;
				this.addWidget("text",name,def_value, { property: name})
			}
		};	
	};

	CustomNode.title = model.name;

	LiteGraph.registerNodeType(`custom/${CustomNode.title}`,CustomNode)
}

export interface pydanticGraph {
	api: Api;
	registerNodes(): void;
	set_download_button(): void;
	setup(): void;
}



class pydanticGraphImpl implements pydanticGraph {
	api: Api;
	graph: any;


    constructor(api: Api) {
		this.api = api;
		this.graph = new LGraph();
		console.log(this.graph.serialize())	
	}


    async registerNodes() {
        // Load node definitions from the backend
        await this.api.fetchNodes()
			.then(defs => defs.forEach(
				(x,i) => modelToNode(x))
			);
    };


	set_download_button(){
		var header = document.getElementById("InstrumentHeader")

		var elem = document.createElement("span");
		elem.id = "InstrumentPanel";
		elem.className = "selector";
		elem.innerHTML = "<button class='btn' id='download'>Download</button>";
		header.appendChild(elem)

		const graph = this.graph

		elem.querySelector("#download").addEventListener("click",function(){
			var data = JSON.stringify(graph.serialize() );
			var file = new Blob( [ data ] );
			var url = URL.createObjectURL( file );
			var element = document.createElement("a");
			element.setAttribute('href', url);
			element.setAttribute('download', "graph.JSON" );
			element.style.display = 'none';
			document.body.appendChild(element);
			element.click();
			document.body.removeChild(element);
			setTimeout( function(){ URL.revokeObjectURL( url ); }, 1000*60 ); //wait one minute to revoke url	
		});

	}

    async setup(){
        await this.registerNodes();
        var canvas = new LGraphCanvas("#mycanvas", this.graph);
		this.set_download_button()
        this.graph.start()
    }

}

export const app = new pydanticGraphImpl(new Api()); 

