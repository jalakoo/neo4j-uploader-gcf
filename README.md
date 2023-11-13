# Neo4j Uploader for Google Cloud Functions
Simple GCF Function for taking JSON payload data and uploading it to a Neo4j Graph Database instance. This function is primarily meant for webhooks with intermittent new data, not for transferring large data sets.

## Running
Run a function: `poetry run functions-framework --target=gcf_upload`

## Notes
Time to process:

neo4j_uploader v0.4.0
- 100 Nodes
- 100 relationships
- 1000 properties
Should take about 6 seconds to upload

- 500 Nodes
- 500 relationships
- 10000 properties
Should take about 6-8 seconds to upload

- 1000 Nodes
- 1000 Relationships
- 10000 Properties
Takes about 10 seconds
