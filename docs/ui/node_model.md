## Graph representation 

Graph representation 

Following of native Litegraph json of node 


```json
{
      "id": 6, # unique id of node
      "type": "events/counter", # name of model
      "pos": [
        864,
        229
      ],
      "size": {
        "0": 140,
        "1": 66
      },
      "flags": {},
      "order": 4,
      "mode": 0,
      "inputs": [
        {
          "name": "inc",
          "type": -1,
          "link": 4
        },
        {
          "name": "dec",
          "type": -1, # not all types are defined
          "link": null
        },
        {
          "name": "reset",
          "type": -1,
          "link": null
        }
      ], # list of all dependecies
      "outputs": [
        {
          "name": "change",
          "type": -1,
          "links": null
        },
        {
          "name": "num",
          "type": "number",
          "links": null
        }
      ], # list of all connection
      "properties": {
        "doCountExecution": false
    }
}
```

As you see it requires machinery for representation in convenient sorted nodes, which

## Formatting


Node can have multiple inputs and outputs.

Output of node can be used in multiple other nodes. One-to-Many
Input, conversely, only handle one connection. Many-to-one

Serialize pydantic model to JSON
and sends to frontend to
Output consist of:
- inputs
    - name
    - type
- outputs
    - name
    - type

should have modifiable