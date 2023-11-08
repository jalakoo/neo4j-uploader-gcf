# Neo4j Uploader for Google Cloud Functions
Simple GCF Function for taking JSON payload data and uploading it to a Neo4j Graph Database instance. This function is primarily meant for webhooks with intermittent new data, not for transferring large data sets.

## Running
Run a function: `poetry run functions-framework --target=gcf_upload`

## Notes
Time to process:

200 Nodes
300 relationships
1300 properties

Currently takes about 15 seconds to process