import logging
import json
from datetime import datetime
import azure.functions as func

def search_title(database: func.DocumentList, title: str) -> dict:
    logging.info("Getting Challenges by title")

    found_challenges = []

    if title == "NONE":
        found_challenges = [
            json.loads(challenge.to_json())
            for challenge in database if actuel(challenge)
        ]
    else:
        for challenge in database:
            if title.lower() in challenge["title"].lower() and actuel(challenge):
                found_challenges.append(json.loads(challenge.to_json()))
        
    return {"found_challenges": found_challenges}


def search_date(database: func.DocumentList, startDate: datetime, endDate: datetime) -> dict:
    logging.info("Getting Challenges by start and end Date")

    found_challenges = []

    for challenge in database:
        if challenge["startDate"] < startDate or challenge["endDate"] > endDate and actuel(challenge):
            found_challenges.append(json.loads(challenge.to_json()))

    return {"found_challenges": found_challenges}


def search_duration(database: func.DocumentList, duration: int) -> dict:
    logging.info("Getting Challenges by duration")
    found_challenges = []

    for challenge in database:
        if abs(challenge["endDate"]-challenge["startDate"]).days <= duration and actuel(challenge):
            found_challenges.append(challenge)
    
    return {"found_challenges": found_challenges}


def search_difficulty(database: func.DocumentList, difficulty_categories:str) -> dict:
    logging.info("Getting Challenges by difficulty")

    difficulties = difficulty_categories.split(",")

    found_challenges = []

    for challenge in database:
        if challenge["difficulty"] in difficulties and actuel(challenge):
            found_challenges.append(challenge)

    return {"found_challenges": found_challenges}


def search_tags(database: func.DocumentList, tags: str) -> dict:
    logging.info("Getting Challenges by tags")
    tag_list = tags.lower().strip().split(",")

    found_challenges = []

    for challenge in database:
        if any([tag in challenge["tags"] for tag in tag_list]) and actuel(challenge):
            found_challenges.append(challenge)

    return {"found_challenges": found_challenges}


def actuel(challenge: dict) -> bool:
    return challenge["endDate"] < datetime.date()