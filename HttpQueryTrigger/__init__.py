import logging
import json
from datetime import datetime

import azure.functions as func


def main(req: func.HttpRequest, database:func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if req.params.get("title"):
        logging.info("Getting Challenges by title")
        title = req.params.get("title")

        found_challenges = []

        if title == "NONE":
            found_challenges = [
                json.loads(challenge.to_json())
                for challenge in database
            ]
        else:
            for challenge in database:
                if title.lower() in challenge["title"].lower():
                    found_challenges.append(json.loads(challenge.to_json()))
            
        result_dict = {"found_challenges": found_challenges}

    elif req.params.get("startDate") and req.params.get("endDate"):
        logging.info("Getting Challenges by start and end Date")
        startDate = datetime.fromisoformat(req.params.get("startDate"))
        endDate = datetime.fromisoformat(req.params.get("endDate"))

        found_challenges = []

        for challenge in database:
            if challenge["startDate"] < startDate or challenge["endDate"] > endDate:
                found_challenges.append(json.loads(challenge.to_json()))

        result_dict = {"found_challenges": found_challenges}

    elif req.params.get("tags[]"):
        logging.info("Getting Challenges by tags")
        tag_list = req.params.get("tags[]").lower().strip().split(",")
        print(tag_list)
        result_dict = {}

    else:
        logging.info("No valid parameter given")
        result_dict = {}

    return func.HttpResponse(
            json.dumps(result_dict),
            status_code=200,
            mimetype="application/json"            
    )