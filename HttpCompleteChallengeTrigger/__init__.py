import logging
import uuid

import azure.functions as func


def main(
    req: func.HttpRequest, 
    resultsdbwrite: func.Out[func.Document],
    resultsdbread: func.DocumentList,
    userdbread: func.DocumentList,
    userdbwrite: func.Out[func.Document],
    challengedbread: func.DocumentList
    ):
    logging.info('Python HTTP trigger function processed a request.')

    request_body = req.get_json()
    logging.info(request_body)
    challenge_id = request_body.get("challenge_id")
    user_id = request_body.get("user_id")
    
    # create challenge result entry
    entry_dict = {
        "id": str(uuid.uuid4()),
        "challenge_id": challenge_id,
        "user_id": user_id,
        "ranking": count_entries(resultsdbread, challenge_id)+1
    }
    logging.info(entry_dict)

    new_challengeresult_docs = func.DocumentList() 
    new_challengeresult_docs.append(func.Document.from_dict(entry_dict))

    resultsdbwrite.set(new_challengeresult_docs)

    # update user score
    user = search(userdbread, "id", user_id)
    challenge_points = search(challengedbread, "id", challenge_id).get("points")

    user["points"] += challenge_points
    user["nChallenges"] += 1

    new_user_docs = func.DocumentList()
    new_user_docs.append(func.Document.from_dict(user))

    userdbwrite.set(new_user_docs)

def count_entries(db: func.DocumentList, entry: str) -> int:
    count = 0
    for collection in db:
        if entry in collection.keys():
            count +=1
    return count

def search(db:func.DocumentList, key: str, value: str) -> dict:
    for entry in db:
        if value == entry[key]:
            return entry
    return 