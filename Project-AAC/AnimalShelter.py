import datetime

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson.objectid import ObjectId
import json


class AnimalShelter(object):
    def __init__(self, user, password, db, col):
        self.user = user
        self.password = password
        self.db = db
        self.col = col

        HOST = "nv-desktop-services.apporto.com"
        PORT = 32061

        self.client = MongoClient(f'mongodb://{user}:{password}@{HOST}:{PORT}')
        print(
            "Connected to client!" if self.client.server_info() else "Connection unsuccessful!")  # --> This forces
        # auth to raise exception if user creds are not valid for client

        self.database = self.client[db]
        self.collection = self.database[col]
        global data
        data = self.database.animals.find({})

    def create(self, data: dict = None) -> bool:
        if data is None:
            data = {}
        if data is not None:
            insert = self.database.animals.insert_one(data)
            print(f"created object for {self.db}.{self.col} \ndata = {data}")
            if insert:
                return True
            else:
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty...")

    def read(self, filter_query: dict = None) -> dict:
        if filter_query is None:
            query = self.database.animals.find({}, {"_id": 0})
        match filter_query:
            case "Show All":
                query = self.database.animals.find({}, {"_id": 0})
            case "Water":
                search = {'$or':
                    [
                        {"breed": "Labrador Retriever Mix"},
                        {"breed": "Chesapeake Bay Retriever"},
                        {"breed": "Newfoundland"}
                    ],
                    "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156},
                    "sex_upon_outcome": "Intact Female"}
                query = self.database.animals.find(search, {"_id": 0})
            case "Mountain":
                search = {'$or':
                              [{"breed": "German Shepherd"},
                               {"breed": "Alaskan Malamute"},
                               {"breed": "Old English Sheepdog"},
                               {"breed": "Siberian Husky"},
                               {"breed": "Rottweiler"}
                               ],
                          "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156},
                          "sex_upon_outcome": "Intact Male"}
                query = self.database.animals.find(search, {"_id": 0})
            case "Disaster":
                search = {'$or':
                              [{"breed": "Doberman Pinscher"},
                               {"breed": "German Shepherd"},
                               {"breed": "Golden Retriever"},
                               {"breed": "Bloodhound"},
                               {"breed": "Rottweiler"}
                               ],
                          "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156},
                          "sex_upon_outcome": "Intact Male"}
                query = self.database.animals.find(search, {"_id": 0})
            case "Elderly":
                search = {"age_upon_outcome_in_weeks": {'$gte': 782}}
                query = self.database.animals.find(search, {"_id": 0})
            case "Spayed Dogs":
                query = self.database.animals.find(
                    {
                        "animal_type": "Dog",
                        "sex_upon_outcome": "Spayed Female"},
                    {
                        "_id": 0}
                )
            case "Neutered Dogs":
                query = self.database.animals.find(
                    {
                        "animal_type": "Dog",
                        "sex_upon_outcome": "Neutered Male"},
                    {
                        "_id": 0}
                )
            case "Neutered Cats":
                query = self.database.animals.find(
                    {
                        "animal_type": "Cat",
                        "sex_upon_outcome": "Neutered Male"},
                    {
                        "_id": 0}
                )
            case "Spayed Cats":
                query = self.database.animals.find(
                    {
                        "animal_type": "Cat",
                        "sex_upon_outcome": "Spayed Female"},
                    {
                        "_id": 0}
                )
            case _:
                print(f'{filter_query} is not a valid filter...')
        return query

    def update(self, query: dict = None, update_to: dict = None) -> dict:
        if update_to is None:
            update_to = {}
        if query is None:
            query = {}
        if query:
            for idx, doc in enumerate(data):
                if doc.get("animal_id") == query["animal_id"]:
                    return self.database.animals.update_many(query, {
                        "$set": update_to,
                        "$currentDate": {"lastModified": True}
                    }).raw_result
        else:
            raise Exception("Nothing to update, because data parameter is empty...")

    def delete(self, query: dict) -> dict:
        if query:
            for idx, doc in enumerate(data):
                if doc.get("animal_id") == query["animal_id"]:
                    return self.database.animals.delete_many(query).raw_result
        else:
            raise Exception("Nothing to delete, because data parameter is empty...")
