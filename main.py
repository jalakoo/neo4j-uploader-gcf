import functions_framework
from neo4j_uploader import batch_upload
import os

@functions_framework.http
def json_to_neo4j(request):

    # Make sure we can extract the JSON payload from the request

    # content_type = request.headers['content-type']
    # if content_type != 'application/json':
    #     return "Content-type must be type application/json", 400
    
    try:
        request_json = request.get_json(silent=True)
    except Exception as e:
        return f"Exception getting JSON: {e}", 400
    
    # Validate config information is available
    uri = os.environ.get('NEO4J_URI', None)
    user = os.environ.get('NEO4J_USERNAME', None)
    password = os.environ.get('NEO4J_PASSWORD', None)
    if uri is None or user is None or password is None:
        return 'Neo4j credentials missing', 500
    
    # Forward the request to the neo4j-uploader
    try:
        upload_result = batch_upload(
            config = {
                'neo4j_uri': uri,
                'neo4j_user': user,
                'neo4j_password': password
            },
            data = request_json
            )
        return upload_result.model_dump(), 200, {"Content-Type": "application/json"}
    except Exception as e:
        return f'Problem uploading: {e}', 500