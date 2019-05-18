import os

import pycountry

from cli.form import Form
from util.file_processing import get_data_from_file
from util.args import Args


class CountryCodesConfigForm(Form):

    def __init__(self, parent: Form):
        self.__parent = parent
        self.__country_codes = set()
        self.__country_codes.add('US')

    def launch(self):
        loop = True
        while loop:
            self.__print__menu()
            choice = input(">>> Enter your choice [0-3]: ")
            if choice == '1':
                self.__add_new_country_codes()

            elif choice == '2':
                self.__add_country_codes_from_file()

            elif choice == '3':
                self.__remove_country_codes()

            elif choice == '4':
                self.__remove_all_country_codes()

            elif choice == '5':
                self.__list_of_country_codes()

            elif choice == '0':
                loop = False

            else:
                print(">>> Wrong option selection!")

            if loop and choice in ['2', '5']:
                input(">>> Press Enter to continue...")

    def __add_new_country_codes(self):
        os.system('cls')
        str_codes = input('Enter country codes to add(delimiter = ","):\n')
        codes = [code.strip() for code in str.split(str_codes, sep=',')]

        self.__add_country_codes(codes)

    def __remove_country_codes(self):
        os.system('cls')
        str_codes = input('Enter country codes to remove(delimiter = ","):\n')
        codes = [str.upper(code.strip()) for code in str.split(str_codes, sep=',')]

        self.__country_codes = self.__country_codes.difference(set(codes))

    def __remove_all_country_codes(self):
        self.__country_codes.clear()

    def __add_country_codes_from_file(self):
        os.system('cls')
        file_path = input(f'Enter file path (Default="{Args.country_codes_path()}"): ')

        if len(file_path) == 0:
            file_path = Args.country_codes_path()

        try:
            self.__add_country_codes(get_data_from_file(file_path))

        except FileNotFoundError as e:
            print(f'{e.strerror}: "{e.filename}"')

    @staticmethod
    def __list_of_country_codes():
        for country in pycountry.countries:
            print(f'{country.name} - {country.alpha_2}')

    def __print__menu(self):
        os.system('cls')
        print('\n', 21 * '-', 'CONFIGURE COUNTY CODES MENU', 21 * '-', '\n')
        print('>>> Your country codes: ', list(self.__country_codes), '\n')
        print('1. Add new country codes')
        print('2. Add codes from file')
        print('3. Remove some country codes')
        print('4. Remove all codes')
        print('5. [HELP] List of country codes')
        print('0. Back')
        print('\n', 70 * '-', '\n')

    @property
    def country_codes(self) -> set:
        return self.__country_codes

    def __add_country_codes(self, codes: list):
        for code in codes:
            code = str.upper(code)
            if pycountry.countries.get(alpha_2=code) is not None:
                self.__country_codes.add(code)
