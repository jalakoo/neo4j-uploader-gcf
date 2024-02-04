# Neo4j Uploader for Google Cloud Functions
Simple GCF Function for taking JSON payload data and uploading it to a Neo4j Graph Database instance. This function is primarily meant for webhooks with intermittent new data, not for transferring large data sets.

## Running Locally
Run a function: `poetry run functions-framework --target=json_to_neo4j`

Default port is 8080
To adjust add `--port=<port_number>`

## Testing Locally
Curl can be used to test the function locally. From this root project folder:
```
curl -X POST https://localhost:8081 -H "Content-Type: application/json" -d @sample.json
```

## Deployting to Google Cloud Function
Can reference this repo by adding it to your [Google Cloud Source Repository](https://source.cloud.google.com/), then referencing it from your [Google Cloud Console: Cloud Functions](https://console.cloud.google.com/functions)

Tested working as a 1st gen function.

## JSON Payload Schema
See the sample.json file
