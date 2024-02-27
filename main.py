from basicauth import decode
from neo4j_uploader import batch_upload, InvalidPayloadError
import functions_framework
import os

@functions_framework.http
def json_to_neo4j(request):

    # Validate config information is available
    uri = os.environ.get('NEO4J_URI', None)
    user = os.environ.get('NEO4J_USERNAME', None)
    password = os.environ.get('NEO4J_PASSWORD', None)

    # Optional Basic Auth
    basic_user = os.environ.get('BASIC_AUTH_USER', None)
    basic_password = os.environ.get('BASIC_AUTH_PASSWORD', None)
    if basic_user and basic_password:
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return 'Missing authorization credentials', 401
        request_username, request_password = decode(auth_header)
        if request_username != basic_user or request_password != basic_password:
            return 'Unauthorized', 401
    
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