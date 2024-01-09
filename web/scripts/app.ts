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

		this.size = this.computeSize();	
	};

	// add helper on hover
	// it will written multiline as usual
	if (model.helper || model.properties) {
		CustomNode.prototype.onDrawBackground = function(ctx){
			if( this.mouseOver){
				ctx.fillStyle = "#AAA";
				let diff =  14;
				// display header if only we have it
				if (model.helper){
					var lines = model.helper.split('\n');
					for (var i = 0; i<lines.length; i++){
						ctx.fillText(lines[i], 0, this.size[1] + diff );
						diff += 14;
					}
				}
				// display properties only if them have description
				for (const [name, prop] of Object.entries(model.properties)){
					if (prop.description){
						ctx.fillText(`@${name}: ${prop.description}`, 0, this.size[1] + diff);
						diff += 14;
					}
				}
			}
		};
	}
	

	CustomNode.title = model.name;

	LiteGraph.registerNodeType(`custom/${CustomNode.title}`,CustomNode)
};

export interface pydanticGraph {
	api: Api;
	registerNodes(): void;
	setup(): void;
};



class pydanticGraphImpl implements pydanticGraph {
	api: Api;
	graph: any;


    constructor(api: Api) {
		this.api = api;
		this.graph = new LGraph();
	}


    async registerNodes() {
        // Load node definitions from the backend
        await this.api.fetchNodes()
			.then(defs => defs?.forEach(
				(x,i) => modelToNode(x),null)
			).catch(
				error => console.log('error is', error)
			)
			;
    };
	
	#load_graph(){

	}


	#set_download_button(){
		var header = document.getElementById("InstrumentHeader")

		var elem = document.createElement("span");
		elem.id = "InstrumentPanel";
		elem.className = "selector";
		elem.innerHTML = (
			"<button class='btn' id='download'>Download</button>\
			<button class='btn' id='validate'>Validate</button>"
		)
		header.appendChild(elem);

		const graph = this.graph;
		const api = this.api;

		elem.querySelector("#download").addEventListener("click",async function(){
			var data: string = JSON.stringify(graph.serialize());
			await api.send_graph_json(data);
		});

		elem.querySelector("#validate").addEventListener("click",async function(){
			var data: string = JSON.stringify(graph.serialize());
			await api.send_graph_json(data);
			alert('Wrong Graph!');
		});

	}

    async setup(){
        await this.registerNodes();
        var canvas = new LGraphCanvas("#mycanvas", this.graph);

		canvas.onDropItem = function(e)
		{
			var that = this;
			for(var i = 0; i < e.dataTransfer.files.length; ++i)
			{
				var file = e.dataTransfer.files[i];
				var ext = LGraphCanvas.getFileExtension(file.name);
				// uploading graph
				if(ext == "json"){
					var reader = new FileReader();
					reader.onload = function(event) {
						var data = JSON.parse( event.target.result as string );
						that.graph.configure(data);
					};
				}
				// uploading new nodes
				else if (ext == "py"){	
					fetch('/parse_nodes', {
						method: 'POST',
						body:  file
					  })
				}
				this.registerNodes();
			}
		}



		this.#set_download_button()
        this.graph.start()
    }

};

export const app = new pydanticGraphImpl(new Api()); 

