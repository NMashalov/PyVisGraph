import {Api, ModelSchema,LocalModuleSchema} from './api.js'

declare var LiteGraph, LGraph, LGraphCanvas;

// var LiteGraph = global.LiteGraph;

function modelToNode(model : ModelSchema,name: string)
{
	console.log(model);
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

		this.properties['hash'] = model.hash;
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
	

	LiteGraph.registerNodeType(`${name}/${CustomNode.title}`,CustomNode)
};

export interface pydanticGraph {
	api: Api;
	setup(): void;
};



class pydanticGraphImpl implements pydanticGraph {
	api: Api;
	graph: any;
	dagName: string;


    constructor(api: Api) {
		this.api = api;
		this.graph = new LGraph();
		this.dagName = 'Dummy'
	}


    async #registerNodes(promise: Promise<Array<LocalModuleSchema>>) {
        // Load node definitions from the backend
        await promise
			.then(
				modules => 
				modules.forEach(
					(module,_) =>
					module.nodes.forEach((x,_) => modelToNode(x,module.module_name))
				),
				null
			).catch(
				error => console.log('error is', error)
			);
    };
	


	#set_header(){
		var header = document.getElementById("InstrumentHeader")

		var elem = document.createElement("span");
		elem.id = "InstrumentPanel";
		elem.className = "selector";
		elem.innerHTML = (
			"<button class='btn' id='download'>Download</button>\
			<button class='btn' id='validate'>Validate</button>\
			<input type='text' id='changeDagName' value='Enter Dag Name'>"
		)
		header.appendChild(elem);

		elem.querySelector("#download").addEventListener("click",async () => {
			var data = {}
			data['graph'] = this.graph.serialize();
			data['dag_name'] = this.dagName;
 
			var response: string = await this.api.send_graph_json(data)
			var file = new Blob( [ response ] );
			var url = URL.createObjectURL(file);
			var element = document.createElement("a");
			element.setAttribute('href', url);
			element.setAttribute('download', "graph.yaml");
			element.style.display = 'none';
			document.body.appendChild(element);
			element.click();
			document.body.removeChild(element);
		});

		elem.querySelector("#validate").addEventListener("click",async () => {
			var data: string = JSON.stringify(this.graph.serialize());
			await this.api.send_graph_json(data);
			alert('Wrong Graph!');
		});


		elem.querySelector("#changeDagName").addEventListener("change", (e: Event & {
			target: HTMLInputElement}) => {
			console.log(e.target.value) 
			this.dagName = e.target.value;
		});

	}

    async setup(){
        await this.#registerNodes(this.api.fetchLocalNodes());
        var canvas = new LGraphCanvas("#mycanvas", this.graph);

		const that = this; 

		canvas.onDropItem = async function(e)
		{
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
					console.log()
					that.#registerNodes(
						that.api.parseNodesFromFile(file)
					);
				}
				
			}
		}
		this.#set_header()
        this.graph.start()
    }

};

export const app = new pydanticGraphImpl(new Api()); 

