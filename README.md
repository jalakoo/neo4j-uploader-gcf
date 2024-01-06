# Neo4j Uploader for Google Cloud Functions
Simple GCF Function for taking JSON payload data and uploading it to a Neo4j Graph Database instance. This function is primarily meant for webhooks with intermittent new data, not for transferring large data sets.

## Running Locally
Run a function: `poetry run functions-framework --target=json_to_neo4j`

Default port is 8080
To adjust use `--port <port_number>`

## Deployting to Google Cloud Function
Can reference this repo by adding it to your [Google Cloud Source Repository](https://source.cloud.google.com/), then referencing it from your [Google Cloud Console: Cloud Functions](https://console.cloud.google.com/functions)

Tested working as a 1st gen function.

## JSON Payload Schema
```
# Example
{
    "config":{
        "neo4j_uri": "{{NEO4J_URI}}",
        "neo4j_user": "{{NEO4J_USER}}",
        "neo4j_password": "{{NEO4J_PASSWORD}}",
        "overwrite": true
    },
    "nodes": [
        {
            "labels":["Person"],
            "key":"uid",
            "records":[
                {
                    "uid":"abc",
                    "name": "John Wick"
                },
                {
                    "uid":"bcd",
                    "name":"Cane"
                }
            ]
        },
        {
            "labels":["Dog"],
            "key": "gid",
            "records":[
                {
                    "gid":"abc",
                    "name": "Daisy"
                }
            ]
        }
    ],
    "relationships": [
        {
            "type":"loves",
            "from_node": {
                "record_key":"_from_uid",
                "node_key":"uid",
                "node_label":"Person"
            },
            "to_node": {
                "record_key":"_to_gid",
                "node_key":"gid",
                "node_label": "Dog"
            },
            "exclude_keys":["_from_uid", "_to_gid"],
            "records":[
                {
                    "_from_uid":"abc",
                    "_to_gid":"abc"
                }
            ]
        }
    ]
}
```
