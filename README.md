# Neo4j Uploader for Google Cloud Functions
Simple GCF Function for taking JSON payload data and uploading it to a Neo4j Graph Database instance. This function is primarily meant for webhooks with intermittent new data, not for transferring large data sets.

## Running Locally
Run a function: `poetry run functions-framework --target=json_to_neo4j`

```
NEO4J_URI=<uri> \
NEO4J_USERNAME=<username> \
NEO4J_PASSWORD=<password> \
poetry run functions-framework --target=json_to_neo4j
```

Optionally enable basic auth by adding in `BASIC_AUTH_USER` and `BASIC_AUTH_PASSWORD` to the env vars:
```
NEO4J_URI=<uri> \
NEO4J_USERNAME=<username> \
NEO4J_PASSWORD=<password> \
BASIC_AUTH_USER=<auth_username> \
BASIC_AUTH_PASSWORD=<auth_password> \
poetry run functions-framework --target=json_to_neo4j
```

Default port is 8080
To adjust add `--port=<port_number>` to the above

## Testing Locally
Curl can be used to test the function locally. From this root project folder:
```
curl -X POST https://localhost:8081 -H "Content-Type: application/json" -d @sample.json
```

## Deployting to Google Cloud Function
Can reference this repo by adding it to your [Google Cloud Source Repository](https://source.cloud.google.com/), then referencing it from your [Google Cloud Console: Cloud Functions](https://console.cloud.google.com/functions)

Tested working as a 1st gen function.

## JSON Payload Schema
```
# Example
{
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
