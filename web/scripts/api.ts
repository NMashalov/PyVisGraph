let API_URL = ''
let API_PORT = "8000"
let NODE_PATH = 'nodes'

export interface Property{
	type: string;
    default_value?: string;
}

export interface Link{
	name: string;
	type: string;
}

export interface ModelSchema{
    name: string;
	input?: Array<Link>;
	output?: Array<Link>;
    properties?: { [name: string]: Property};
}


export class Api{
    url: string;

    constructor(){
        this.url = `${API_URL}:${API_PORT}/${NODE_PATH}`
        console.log(this.url)
    }

    async send_graph_json(graph_json: string){
        await fetch('/graphs', {
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
        });
    }
    async fetchNodes(){
        let data: Array<ModelSchema>  = await fetch('/nodes')
            .then(response => {
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

