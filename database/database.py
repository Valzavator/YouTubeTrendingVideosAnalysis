import datetime
import os
import subprocess

import pymongo
from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.errors import DuplicateKeyError, BulkWriteError

from util.args import Args


class Database:
    def __init__(self, uri=Args.db_uri()):
        self.__client = MongoClient(uri)

        self.__db = self.__client["videos_analysis"]

        self.__videos_coll = self.__db["videos"]
        self.__videos_coll.create_index([("county_code", pymongo.DESCENDING)])

        self.__mongodump_path = "C:\\Program Files\\MongoDB\\Server\\4.0\\bin\\mongodump.exe"
        self.__mongorestore_path = "C:\\Program Files\\MongoDB\\Server\\4.0\\bin\\mongorestore.exe"

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

    def get_videos_by_country_code(self, country_code: str) -> Cursor:
        return self.__videos_coll.find({'country_code': country_code})

    def get_videos_by_country_codes(self, country_codes: list) -> Cursor:
        return self.__videos_coll.find({'country_code': {'$in': country_codes}})

    def remove_all_documents(self):
        self.__videos_coll.remove()

    def count(self):
        return self.__videos_coll.count()

    def get_all_country_codes(self) -> list:
        return list(self.__videos_coll.distinct('country_code'))

    def backup_database(self):
        if not os.path.exists(Args.backup_db_dir()):
            os.makedirs(Args.backup_db_dir())

        cns_command = f'"{self.__mongodump_path}" --collection videos --db videos_analysis' \
            f' --out "{os.path.abspath(Args.backup_db_dir())}"'

        subprocess.check_output(cns_command)

    def restore_database(self):
        if not os.path.exists(Args.backup_db_dir()):
            os.makedirs(Args.backup_db_dir())

        cns_command = f'"{self.__mongorestore_path}" "{os.path.abspath(Args.backup_db_dir())}"'

        subprocess.check_output(cns_command)

    def close(self):
        self.__client.close()
