import os
import subprocess


from cli.form import Form
from database.database import Database
from processing_tool.data_preprocessing import match_category_id_with_category_title
from processing_tool.scraper import YouTubeTrendingVideosScraper
from util.args import Args
from util.file_processing import get_videos_data_from_csv
from requests.exceptions import ConnectionError


class DatabaseManagementForm(Form):

    def __init__(self, parent: Form, database: Database, county_codes: set):
        self.__parent = parent
        self.__db = database
        self.__country_codes = county_codes
        self.__scraper = YouTubeTrendingVideosScraper()

        self.__mongodump_path = "C:\\Program Files\\MongoDB\\Server\\4.0\\bin\\mongodump.exe"
        self.__mongorestore_path = "C:\\Program Files\\MongoDB\\Server\\4.0\\bin\\mongorestore.exe"

    def launch(self):
        loop = True
        while loop:
            self.__print__menu()
            choice = input(">>> Enter your choice [0-2,9]: ")
            if choice == '1':
                try:
                    self.__load_from_youtube()
                except ConnectionError as e:
                    print('Check connection to Internet!')

            elif choice == '2':
                self.__load_from_datasets()

            elif choice == '3':
                self.__backup_database()

            elif choice == '4':
                self.__restore_database()

            elif choice == '9':
                self.__remove_all_documents()

            elif choice == '0':
                loop = False

            else:
                print(">>> Wrong option selection!")

            if loop:
                input(">>> Press Enter to continue...")

    def __load_from_youtube(self):
        os.system('cls')
        print('Please, wait...')

        if len(self.__country_codes) == 0:
            print('Please, choose some country codes!')
            return

        data = self.__scraper.get_videos_data_by_country_codes(self.__country_codes)
        match_category_id_with_category_title(data)

        print(f'\nDownload {len(data)} documents from YouTube Data API.')

        count_of_stored_doc = self.__db.save_many_videos(data)

        print(f'{count_of_stored_doc} unique documents were stored in the database.\n')

    def __load_from_datasets(self):
        os.system('cls')

        all_datasets_path = {
            'CA': 'resource/raw_data/CA_videos.csv',
            'DE': 'resource/raw_data/DE_videos.csv',
            'FR': 'resource/raw_data/FR_videos.csv',
            'GB': 'resource/raw_data/GB_videos.csv',
            'IN': 'resource/raw_data/IN_videos.csv',
            'US': 'resource/raw_data/US_videos.csv'}

        str_codes = input('Available datasets: CA, DE, FR, GB, IN, US.\n'
                          'Enter country codes to load data from dataset(delimiter = ","):\n')

        if str_codes == "":
            codes = all_datasets_path.keys()
        else:
            codes = [str.upper(code.strip()) for code in str.split(str_codes, sep=',')]

        total_count = 0

        for code in codes:
            if code in all_datasets_path:
                path = all_datasets_path.get(code)
                print(f'\n>>> "{path}"')

                data = get_videos_data_from_csv(path)

                print(f'Download {len(data)} documents from csv.')

                count_of_stored_doc = self.__db.save_many_videos(data)
                total_count += count_of_stored_doc

                print(f'{count_of_stored_doc} unique documents were stored in the database.')
            else:
                print(f'>>> Dataset with "{code}" code does not available!')

        print(f'\n>>> Total count: {total_count}\n')

    def __backup_database(self):
        os.system('cls')

        self.__db.backup_database()

    def __restore_database(self):
        os.system('cls')

        self.__db.restore_database()

    def __remove_all_documents(self):
        os.system('cls')
        count_of_documents = self.__db.count()

        if count_of_documents > 0:
            print('Please, wait...')
            self.__db.remove_all_documents()
            print(f'{count_of_documents} documents have been deleted successfully!')
        else:
            print('Database is already clean!')

    def __print__menu(self):
        os.system('cls')
        print('\n', 22 * '-', 'DATABASE MANAGEMENT MENU', 22 * '-', '\n')
        print('>>> Your country codes: ', list(self.__country_codes), '\n')
        print('1. Download from YouTube << for presentation only >>')
        print('2. Download from datasets')
        print('3. Backup database')
        print('4. Restore database')
        print('9. Remove all documents in database')
        print('0. Back')
        print('\n', 70 * '-', '\n')
