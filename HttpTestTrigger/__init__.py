import logging
import json

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    body = req.get_json()
    value = body.get('value')

    result = {"value": value}

    return func.HttpResponse(json.dumps(result))