// @ts-check

function NodeCallback(value, widget, node){
	fetch(
		"127.0.0.1", {
		method: "POST",
		body: JSON.stringify({
			node
		}),
		headers: {
			"Content-type": "application/json; charset=UTF-8"
		}
		}
	)
	.then((response) => response.json())
	.then((json) => console.log(json))
};


class ComfyApi extends EventTarget {

    #registered = new Set();

    constructor() {
		super();
		this.api_host = location.host;
		this.api_base = location.pathname.split('/').slice(0, -1).join('/');
	}


	create_node(json){
		function MyAddNode()
		{

			this.slider_widget = this.addWidget(
				"slider",
				"Slider",
				 0.5,
				 NodeCallback
				, { min: 0, max: 1} s
				);
		}
	}

	callback = (update) => {
		

}

export const api = new ComfyApi();