import functions_framework
from neo4j_uploader import batch_upload, InvalidPayloadError
import os
import logging


@functions_framework.http
def test(request):
    return f'Hello World!', 200

@functions_framework.http
def json_to_neo4j(request):

    logging.info(f'Request received: {request}')

    json = request.get_json()

    config = json.get('config', None)
    if config is None:
        return f'JSON payload missing or malformed. Neo4j config is required', 400
    
    data = json.get('data', None)
    if data is None:
        return f'JSON payload missing or malformed. Nodes and Relationship data is required', 400
    
    # Forward the request to the neo4j-uploader
    try:
        upload_result = batch_upload(
            config = config,
            data = data,
            )
        return upload_result.model_dump(), 200, {"Content-Type": "application/json"}
    except InvalidPayloadError as e:
        # Missing or Invalid JSON payload
        return f'JSON payload missing or malformed. {e}', 400
    except Exception as e:
        # Other neo4j exception or uploader error
        return f'Problem uploading: {e}', 500