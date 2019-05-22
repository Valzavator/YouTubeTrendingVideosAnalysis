import argparse
import os
from dotenv import load_dotenv

load_dotenv()


class Args(object):
    __api_key = None
    __country_codes_path = None
    __raw_data_dir = None
    __category_id_file_path = None
    __analysis_res_dir = None
    __backup_db_dir = None

    @classmethod
    def api_key(cls):
        if cls.__api_key is None:
            cls.__process_arguments()
        return cls.__api_key

    @classmethod
    def country_codes_path(cls):
        if cls.__country_codes_path is None:
            cls.__process_arguments()
        return cls.__country_codes_path

    @classmethod
    def raw_data_dir(cls):
        if cls.__raw_data_dir is None:
            cls.__process_arguments()
        return cls.__raw_data_dir

    @classmethod
    def category_id_file_path(cls):
        if cls.__category_id_file_path is None:
            cls.__process_arguments()
        return cls.__category_id_file_path

    @classmethod
    def analysis_res_dir(cls):
        if cls.__analysis_res_dir is None:
            cls.__process_arguments()
        return cls.__analysis_res_dir

    @classmethod
    def backup_db_dir(cls):
        if cls.__backup_db_dir is None:
            cls.__process_arguments()
        return cls.__backup_db_dir

    @classmethod
    def __process_arguments(cls):
        parser = argparse.ArgumentParser()

        parser.add_argument('--api_key',
                            help='Path to the file containing the api key, '
                                 'by default will use API_KEY value in .env',
                            default=os.getenv('API_KEY'))

        parser.add_argument('--country_codes_path',
                            help='Path to the file containing the list of country codes to scrape, '
                                 'by default will use "country_codes.txt" value',
                            default='country_codes.txt')

        parser.add_argument('--raw_data_dir',
                            help='Path to save the outputted files in, '
                                 'by default will use "resource/raw_data/" value',
                            default=f'resource{os.sep}raw_data{os.sep}')

        parser.add_argument('--category_id_file_path',
                            help='Path to file containing categories naming and their id, '
                                 'by default will use "resource/category/US_category_id.json" value',
                            default=f'resource{os.sep}category{os.sep}US_category_id.json')

        parser.add_argument('--analysis_res_dir',
                            help='Path to file containing result of data analysis, '
                                 'by default will use "resource/analysis_result/" value',
                            default=f'resource{os.sep}analysis_result')

        parser.add_argument('--backup_db_dir',
                            help='Path to file containing result of data analysis, '
                                 'by default will use "resource/backup_database/" value',
                            default=f'resource{os.sep}backup_database')

        args = parser.parse_args()

        cls.__api_key = args.api_key
        cls.__country_codes_path = args.country_codes_path
        cls.__raw_data_dir = args.raw_data_dir
        cls.__category_id_file_path = args.category_id_file_path
        cls.__analysis_res_dir = args.analysis_res_dir
        cls.__backup_db_dir = args.backup_db_dir
