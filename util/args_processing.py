import argparse
import os
from dotenv import load_dotenv

load_dotenv()


def process_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('--api_key',
                        help='Path to the file containing the api key, by default will use api_key.txt '
                             'in the same directory',
                        default=os.getenv('API_KEY'),)

    # parser.add_argument('--country_code_path',
    #                     help='Path to the file containing the list of country codes to scrape, '
    #                          'by default will use country_codes.txt in the same directory',
    #                     default=os.getenv('COUNTRY_CODE_PATH'))

    parser.add_argument('--raw_data_dir',
                        help='Path to save the outputted files in',
                        default=os.getenv('RAW_DATA_DIR'))

    args = parser.parse_args()

    return args
