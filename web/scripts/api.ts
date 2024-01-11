let API_URL = ''
let API_PORT = "8000"
let NODE_PATH = 'nodes'

export interface Property{
	type: string;
    default_value?: string;
    description?: string;
}

export interface Link{
	name: string;
	type: string;
}

export interface ModelSchema{
    name: string;
    hash: string;
	input?: Array<Link>;
	output?: Array<Link>;
    properties?: { [name: string]: Property};
    helper?: String
}

export interface LocalModuleSchema{
    nodes: Array<ModelSchema>;
    module_name: string
}


export class Api{
    url: string;

    constructor(){
        this.url = `${API_URL}:${API_PORT}/${NODE_PATH}`
        console.log(this.url)
    }

    async send_graph_json(graph_json: {}){
        return await fetch('/graphs', {
            method: 'POST', // или 'PUT'
            body: JSON.stringify({
                body: graph_json, // данные могут быть 'строкой' или {объектом}!
                headers: {
                  'Content-Type': 'application/json'
                }
            }), // данные могут быть 'строкой' или {объектом}!
            headers: {
            'Content-Type': 'application/json'
            }
        }).then(response => {
            if (response.ok) {
                return response.json()
            } 
            else if(response.status === 404) {
                return Promise.reject('error 404')   
            }
        },null)
    };
    
    async parseNodesFromFile(file){
        const formData = new FormData();
    	formData.append("file", file, file.name);
        return  await fetch('/parse_nodes', {
            method: 'POST',
            body:  formData
        }).then(response => {
            if (response.ok) {
                return response.json()
            } 
            else if(response.status === 404) {
                return Promise.reject('error 404')   
            }
        },null)
    }

    
    async fetchLocalNodes(){
        let data: Array<LocalModuleSchema> = await fetch('/local_nodes')
            .then(async response => {
                    if (response.ok) {
                        return response.json()
                    } 
                    else if(response.status === 404) {
                        return Promise.reject('error 404')   
                    }
            },null)

        return data 
    }
}

