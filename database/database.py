import datetime

import pymongo
from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.errors import DuplicateKeyError, BulkWriteError


class Database:
    def __init__(self, uri="mongodb://localhost:27017/"):
        self.__client = MongoClient(uri)

        self.__db = self.__client["videos_analysis"]

        self.__videos_coll = self.__db["videos"]
        self.__videos_coll.create_index([("county_code", pymongo.DESCENDING)])

    def __del__(self):
        self.close()

    def save_one_video(self, video: dict) -> bool:

        if video is None:
            return False

        try:
            self.__videos_coll.insert_one(video)
            return True
        except DuplicateKeyError as e:
            print(e)
            return False

    def save_many_videos(self, videos: list, ordered=False) -> int:

        if videos is None or len(videos) == 0:
            return 0

        is_repeat = False

        quantity_before = self.__videos_coll.count()

        try:
            self.__videos_coll.insert_many(videos, ordered=ordered)
        except BulkWriteError as e:
            if ordered:
                raise e
            is_repeat = True

        if is_repeat:
            return self.__videos_coll.count() - quantity_before
        else:
            return len(videos)

    def get_all_videos(self) -> Cursor:
        return self.__videos_coll.find()

    def get_videos_by_countries(self, country_codes: list) -> Cursor:
        return self.__videos_coll.find({'country_code': {'$in': country_codes}})

    def remove_all_documents(self):
        self.__videos_coll.remove()

    def count(self):
        return self.__videos_coll.count()

    def close(self):
        self.__client.close()

    # def select_database(self, database: str):
    #     self.__db = self.__client[database]
    #     self.__videos_coll = self.__db.videos
