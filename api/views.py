from flask import Blueprint, request, Response
from generate import generate
from urllib.parse import unquote
import json

views = Blueprint("views", __name__, url_prefix='/playlist')

@views.route("/<string:link_playlist>", methods=["GET"])
def gen_playlist(link_playlist):
    # body = request.get_json()
    if not link_playlist:
        return gen_response(400, "URL não encontrada")

    if request.method == "GET":
        response = generate(unquote(link_playlist))
        if response:
            return gen_response(200, "Lista dos vídeos da playlist gerado", "videos" ,response)
        else:
            return gen_response(400, "URL não encontrada")

def gen_response(status, message, content_name=False, content_body=False):
    body = {}
    body["status"] = status
    body["message"] = message

    if(content_name and content_body):
        body[content_name] = content_body

    # return json.dumps(body)
    return Response(json.dumps(body), mimetype="application/json", headers={'Access-Control-Allow-Origin':'*'})