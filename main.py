import functions_framework
from pydantic import BaseModel, validator, parse_obj_as
from neo4j_uploader import upload, start_logging
import logging
import json

logging.getLogger().setLevel(logging.DEBUG)
logging.info(f'App Started')

class CreateDynamicRequest(BaseModel):
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    data: dict
    node_key :str = "_uid"
    dedupe: bool = False
    # @validator("neo4j_uri", "neo4j_user", "neo4j_password", pre=True, always=True)
    # def convert_to_none(cls, value):
    #     if isinstance(value, str) and value.strip() == "":
    #         return None
    #     return value

@functions_framework.http
def gcf_upload(request):
    content_type = request.headers['content-type']
    if content_type != 'application/json':
        return "Content-type must be type application/json"
    
    try:
        request_json = request.get_json(silent=True)
    except Exception as e:
        print(f'Exception getting JSON: {e}')
        return "Exception getting JSON", 400
    
    print(f'received json: {request_json}')
    start_logging()

    # Why isn't Pydantic working here?
    # nRequest = CreateDynamicRequest.model_validate(request_json)
    
    uri = request_json.get('neo4j_uri')
    user = request_json.get('neo4j_user')
    password = request_json.get('neo4j_password')
    node_key = request_json.get('node_key', "_uid")
    dedupe = request_json.get('dedupe', False)
    data = request_json.get('data')

    print(f'uri: {uri}, user: {user}, pass: {password}, node_key:{node_key}, data:{data}')

    try:
        time, nodes_created, rel_created, props_set = upload((uri, user, password), data, node_key=node_key, dedupe_nodes=dedupe, dedupe_relationships = dedupe)
        return json.dumps({'seconds_to_complete': time, 'nodes_created': nodes_created,'rel_created': rel_created, 'props_set': props_set}), 200, {"Content-Type": "application/json"}
    except Exception as e:
        return f'Problem uploading: {e}', 500
