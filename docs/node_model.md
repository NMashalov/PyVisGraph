Example of native json of node 

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