import os

from cli.analyze_data_from import AnalyzeDataForm
from cli.country_codes_config_form import CountryCodesConfigForm
from cli.database_management_form import DatabaseManagementForm
from cli.form import Form
from database.database import Database


class YouTubeTrendingAnalysisApplication(Form):

    def __init__(self):
        self.__db = Database()

        self.__codes_config = CountryCodesConfigForm(self, self.__db)
        self.__database_management = DatabaseManagementForm(self, self.__db, self.__codes_config.country_codes)
        self.__analyze_data = AnalyzeDataForm(self, self.__db, self.__codes_config.country_codes)

    def launch(self):
        loop = True

        while loop:

            self.__print__menu()
            choice = input(">>> Enter your choice [0-3]: ")

            if choice == '1':
                self.__codes_config.launch()

            elif choice == '2':
                self.__database_management.country_codes = self.__codes_config.country_codes
                self.__database_management.launch()

            elif choice == '3':
                self.__analyze_data.country_codes = self.__codes_config.country_codes
                self.__analyze_data.launch()

            elif choice == '0':
                self.__db.close()
                loop = False

            else:
                print(">>> Wrong option selection!")

            if not loop:
                print('>>> Bye, bye...')

    @staticmethod
    def __print__menu():
        os.system('cls')
        print('\n', 30 * '-', 'MAIN MENU', 30 * '-', '\n')
        print('1. Configure country codes')
        print('2. Database management ')
        print('3. Analyze data')
        print('0. Exit')
        print('\n', 71 * '-', '\n')
