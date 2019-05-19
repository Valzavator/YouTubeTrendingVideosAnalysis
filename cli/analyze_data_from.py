import os
import subprocess
import time

import pandas as pd
from pandas import DataFrame

from cli.form import Form
from database.database import Database
from processing_tool.data_analysis import correlation, category_rating, distribution_boxplot, distribution_plot, \
    distribution_of_days, distribution_of_days_preprocessing, fastest_grow_among_categories, top_channels
from util.args import Args


class AnalyzeDataForm(Form):

    def __init__(self, parent: Form, database: Database, county_codes: set):
        self.__parent = parent
        self.__db = database
        self.__country_codes = county_codes

    def launch(self):
        loop = True
        while loop:
            self.__print__menu()
            choice = input(">>> Enter your choice [0-3]: ")
            if choice == '1':
                self.__general_analysis()

            elif choice == '2':
                self.__detailed_analysis_for_each_country_separately()

            elif choice == '3':
                self.__detailed_analysis_for_all_countries()

            elif choice == '0':
                loop = False

            else:
                print(">>> Wrong option selection!")

            if loop and choice in ['1']:
                input(">>> Press Enter to continue...")

    def __general_analysis(self):
        data = self.__db.get_videos_by_countries(list(self.__country_codes))

        data_frame = pd.DataFrame(data)
        #
        # data = distribution_of_days_preprocessing(data_frame)
        # print(data.head(10).to_string())

        # fastest_grow_among_categories(data_frame)
        top_channels(data_frame, 10)

    def __detailed_analysis_for_each_country_separately(self):
        for code in self.__country_codes:
            data = self.__db.get_videos_by_countries(list(self.__country_codes))

            data_frame = pd.DataFrame(data)

            if data_frame.size == 0:
                print(f'No data for analysis {code}!')
                continue

            output_directory = os.path.join(
                Args.analysis_res_dir(),
                f'{code}{os.sep}{time.strftime("%d.%m.%y")}{os.sep}')

            self.__detailed_analysis_for_data(data_frame, output_directory)

        subprocess.Popen(f'explorer /select, {Args.analysis_res_dir()}{os.sep}')

    def __detailed_analysis_for_all_countries(self):
        data = self.__db.get_videos_by_countries(list(self.__country_codes))

        data_frame = pd.DataFrame(data)

        if data_frame.size > 0:
            output_directory = os.path.join(
                Args.analysis_res_dir(),
                f'all_country{os.sep}{time.strftime("%d.%m.%y")}{os.sep}')

            self.__detailed_analysis_for_data(data_frame, output_directory)

            subprocess.Popen(f'explorer /select, {output_directory}')
        else:
            print('No data for analysis!')

    @staticmethod
    def __detailed_analysis_for_data(data_frame: DataFrame, output_dir):
        correlation(data_frame, output_dir)
        category_rating(data_frame, output_dir)
        distribution_boxplot(data_frame, output_dir)
        distribution_plot(data_frame, output_dir)
        distribution_of_days(data_frame, output_dir)

    def __print__menu(self):
        os.system('cls')

        print('\n', 25 * '-', 'DATA ANALYSIS MENU', 25 * '-', '\n')
        print('>>> Your country codes: ', list(self.__country_codes), '\n')
        print('1. General analysis')
        print('2. Detailed analysis for each country separately')
        print('3. Detailed analysis for all countries together')
        print('0. Back')
        print('\n', 70 * '-', '\n')
