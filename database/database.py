from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError


class Database:
    def __init__(self, to_clear=False, uri="mongodb://localhost:27017/"):
        self.__client = MongoClient(uri)

        self.__db = self.__client["videos_analysis"]

        self.__videos_coll = self.__db["videos"]

        if to_clear:
            self.clear_database()

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

    def get_videos(self) -> list:
        return list(self.__videos_coll.find())

    def clear_database(self):
        self.__videos_coll.remove()

    def close(self):
        self.__client.close()

    # def select_database(self, database: str):
    #     self.__db = self.__client[database]
    #     self.__videos_coll = self.__db.videos
