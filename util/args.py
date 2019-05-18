import argparse
import os
from dotenv import load_dotenv

load_dotenv()


class Args(object):

    _api_key = None
    _country_codes_path = None
    _raw_data_dir = None
    _category_id_file_path = None

    @classmethod
    def api_key(cls):
        if cls._api_key is None:
            cls.__process_arguments()
        return cls._api_key

    @classmethod
    def country_codes_path(cls):
        if cls._country_codes_path is None:
            cls.__process_arguments()
        return cls._country_codes_path

    @classmethod
    def raw_data_dir(cls):
        if cls._raw_data_dir is None:
            cls.__process_arguments()
        return cls._raw_data_dir

    @classmethod
    def category_id_file_path(cls):
        if cls._category_id_file_path is None:
            cls.__process_arguments()
        return cls._category_id_file_path

    @classmethod
    def __process_arguments(cls):
        parser = argparse.ArgumentParser()

        parser.add_argument('--api_key',
                            help='Path to the file containing the api key, '
                                 'by default will use API_KEY value in .env',
                            default=os.getenv('API_KEY'), )

        parser.add_argument('--country_codes_path',
                            help='Path to the file containing the list of country codes to scrape, '
                                 'by default will use COUNTRY_CODES_PATH value in .env',
                            default=os.getenv('COUNTRY_CODES_PATH'))

        parser.add_argument('--raw_data_dir',
                            help='Path to save the outputted files in, '
                                 'by default will use RAW_DATA_DIR value in .env',
                            default=os.getenv('RAW_DATA_DIR'))

        parser.add_argument('--category_id_file_path',
                            help='Path to file containing categories naming and their id, '
                                 'by default will use CATEGORY_ID_FILE_PATH value in .env',
                            default=os.getenv('CATEGORY_ID_FILE_PATH'))

        args = parser.parse_args()

        cls._api_key = args.api_key
        cls._country_codes_path = args.country_codes_path
        cls._raw_data_dir = args.raw_data_dir
        cls._category_id_file_path = args.category_id_file_path
