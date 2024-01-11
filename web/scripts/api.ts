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
        }).then(async response => {
            if (response.ok) {
                alert('ok')
                return response.json()
            } 
            else if(response.status === 404) {
                return Promise.reject('error 404')   
            }
            else if (response.status === 418){
                let j: [{}] = JSON.parse(await response.json())
                let alert_msg = ''
                j.forEach((el,i)=>{
                    alert_msg += `Error. Field ${el['loc']} has received msg ${el['msg']}\n`
                })
                alert(alert_msg);
            }
            else if (response.status === 421){
                let j: [{}] = await response.json()
                alert(j);
            }
            else if (response.status === 500){
                alert('500 Server Error')
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
    
    async fetchDagSettings(){
        let data : { [name: string]: string} = await fetch('/dag_fields')
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

