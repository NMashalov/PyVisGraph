let API_URL = '127.0.0.1'
let API_PORT = "8080"
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
    url: string

    constructor(){
        this.url = `${API_URL}:${API_PORT}/${NODE_PATH}`

    }
    async fetchNodes(){
        let data = (await fetch(this.url)).json()
        return data 
    }
}
