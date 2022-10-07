import logging
import json
from datetime import datetime

import azure.functions as func
from HttpQueryTrigger.challengefilter import search_duration

from . import challengefilter as cf


def main(req: func.HttpRequest, database:func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if req.params.get("title"):
        result_dict = cf.search_title(
            database=database, 
            title=req.params.get("title")
    )
        
    elif req.params.get("startDate") and req.params.get("endDate"):
        result_dict = cf.search_date(
            database=database,
            startDate=datetime.fromisoformat(req.params.get("startDate")),
            endDate=datetime.fromisoformat(req.params.get("endDate"))
            )
    
    elif req.params.get("duration"):
        result_dict = cf.search_duration(
            database=database, 
            duration=req.params.get("duration")
        )
    
    elif req.params.get("difficulty"):
        result_dict = cf.search_difficulty(
            database=database,
            difficulty_categories=req.params.get("difficulty")
        )


    elif req.params.get("tags[]"):
        result_dict = cf.search_tags(
            datebase=database,
            tags=req.params.get("tags[]")
        )

    else:
        logging.info("No valid parameter given")
        result_dict = {}

    return func.HttpResponse(
            json.dumps(result_dict),
            status_code=200,
            mimetype="application/json"            
    )