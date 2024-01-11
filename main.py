import functions_framework
from neo4j_uploader import batch_upload, InvalidPayloadError
import os

@functions_framework.http
def json_to_neo4j(request):

    # Validate config information is available
    uri = os.environ.get('NEO4J_URI', None)
    user = os.environ.get('NEO4J_USERNAME', None)
    password = os.environ.get('NEO4J_PASSWORD', None)
    
    # Forward the request to the neo4j-uploader
    try:
        upload_result = batch_upload(
            config = {
                'neo4j_uri': uri,
                'neo4j_user': user,
                'neo4j_password': password
            },
            data = request.get_json(silent=True),
            )
        return upload_result.model_dump(), 200, {"Content-Type": "application/json"}
    except InvalidPayloadError as e:
        # Missing or Invalid JSON payload
        return f'JSON payload missing or malformed. {e}', 400
    except Exception as e:
        # Other neo4j exception or uploader error
        return f'Problem uploading: {e}', 500