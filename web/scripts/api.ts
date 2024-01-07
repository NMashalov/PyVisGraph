let API_URL = ''
let API_PORT = "8000"
let NODE_PATH = 'nodes'

export interface Property{
	name: string;
	type: string;
}

export interface Link{
	name: string;
	type: string;
}

export interface ModelSchema{
    name: string;
	input?: Array<Link>;
	output?: Array<Link>;
    properties?: Array<Property>;
}


export class Api{
    url: string;

    constructor(){
        this.url = `${API_URL}:${API_PORT}/${NODE_PATH}`
        console.log(this.url)
    }
    async fetchNodes(){
        let data: Array<ModelSchema>  = await fetch('/nodes')
            .then(response => response.json())
        return data 
    }
}

