import os
import subprocess
import time
import pycountry
import gc
import pandas as pd
from pandas import DataFrame

from cli.form import Form
from database.database import Database
import processing_tool.data_analysis as da
from util.args import Args


class AnalyzeDataForm(Form):

    def __init__(self, parent: Form, database: Database, county_codes: set):
        self.__parent = parent
        self.__db = database
        self.__country_codes = county_codes

    def launch(self):
        loop = True
        while loop:
            try:
                self.__print__menu()
                choice = input(">>> Enter your choice [0-3]: ")
                if choice == '1':
                    self.__detailed_analysis_for_each_country_separately()

                elif choice == '2':
                    if len(self.__country_codes) > 1:
                        self.__detailed_analysis_for_all_countries()
                    elif len(self.__country_codes) == 1:
                        self.__detailed_analysis_for_each_country_separately()

                elif choice == '0':
                    loop = False

                else:
                    print(">>> Wrong option selection!")

                if loop:
                    input(">>> Press Enter to continue...")

            except MemoryError:
                print(">>> RAM overflow!")
                input(">>> Try again...")

            gc.collect()

    def __detailed_analysis_for_each_country_separately(self):
        os.system('cls')
        print('Please, wait...')

        is_analyze = False

        for code in self.__country_codes:

            print(f'COUNTRY: {pycountry.countries.get(alpha_2=code).name}')

            data = self.__db.get_videos_by_country_code(code)
            data_frame = pd.DataFrame(data)

            del data

            if data_frame.size == 0:
                print(f'No data for analysis {code}!')
                continue

            is_analyze = True

            output_directory = os.path.join(
                Args.analysis_res_dir(),
                f'{code}{os.sep}{time.strftime("%d.%m.%y")}{os.sep}')

            print('>>> General analysis is carried out')
            self.__general_analysis_for_data(data_frame, output_directory)
            print('>>> General report is completed!')

            print('>>> Detailed analysis is carried out')
            self.__detailed_analysis_for_data(data_frame, output_directory)
            print('>>> Detailed analysis is completed!')

            del data_frame

        if is_analyze:
            os.startfile(Args.analysis_res_dir())
            # subprocess.Popen(f'explorer /select, {Args.analysis_res_dir()}{os.sep}')

    def __detailed_analysis_for_all_countries(self):
        os.system('cls')
        print('Please, wait...')

        data = self.__db.get_videos_by_country_codes(list(self.__country_codes))
        data_frame = pd.DataFrame(data)

        del data

        if data_frame.size > 0:
            output_directory = os.path.join(
                Args.analysis_res_dir(),
                f'all_country{os.sep}{time.strftime("%d.%m.%y")}{os.sep}')

            print('>>> General analysis is carried out')
            self.__general_analysis_for_data(data_frame, output_directory)
            print('>>> General report is completed!')

            print('>>> Detailed analysis is carried out')
            self.__detailed_analysis_for_data(data_frame, output_directory)
            print('>>> Detailed analysis is completed!')

            # subprocess.Popen(f'explorer /select, {output_directory}')
            os.startfile(output_directory)
        else:
            print('No data for analysis!')

        del data_frame

    def __general_analysis_for_data(self, data_frame: DataFrame, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, 'general_analysis.txt')

        with open(file_path, "w+",
                  encoding='utf-8') as file:
            ###

            file.write(f"{20 * '-'} {str.upper('General information')} {20 * '-'}\n\n")
            data_frame.info(buf=file)

            ###

            file.write(self.__create_paragraph(
                'General view of the four numeric attributes',
                data_frame[['view_count', 'likes', 'dislikes', 'comment_count']].describe()))

            ###

            data_frame = da.distribution_of_days_preprocessing(data_frame)

            file.write(self.__create_paragraph(
                'Distribution of days that videos take to become popular',
                data_frame.interval.describe()))

            ###

            file.write(self.__create_paragraph(
                'Top videos whose << view_count >> grow fastest among categories',
                da.view_count_fastest_grow_among_categories(data_frame, preprocessing=False).to_string()))

            ###

            file.write(self.__create_paragraph(
                'Top videos whose << likes >> grow fastest among categories',
                da.likes_fastest_grow_among_categories(data_frame, preprocessing=False).to_string()))

            ###

            file.write(self.__create_paragraph(
                'Top videos whose << dislikes >> grow fastest among categories',
                da.dislikes_fastest_grow_among_categories(data_frame, preprocessing=False).to_string()))

            ###

            file.write(self.__create_paragraph(
                'Top videos whose << comment_count >> grow fastest among categories',
                da.comment_count_fastest_grow_among_categories(data_frame, preprocessing=False).to_string()))

            file.write(self.__create_paragraph(
                'Top channels',
                da.top_channels(data_frame, 100).to_string()))

            file.close()

        gc.collect()

    @staticmethod
    def __detailed_analysis_for_data(data_frame: DataFrame, output_dir):

        analysis_funcs = [
            da.views_likes_dislikes_comments_normal_distribution,
            da.correlation,
            da.category_rating,
            da.distribution_boxplot,
            da.distribution_plot,
            da.distribution_of_days,
            da.word_cloud_for_tags,
            da.word_cloud_for_titles,
            da.word_cloud_for_description,
            # da.sentiment_analysis
        ]

        i = 0
        for funcs in analysis_funcs:
            funcs(data_frame, output_dir)
            i += 1
            print(f'... [{int(i*100/len(analysis_funcs))} %]')
            gc.collect()

    def __print__menu(self):
        os.system('cls')

        print('\n', 25 * '-', 'DATA ANALYSIS MENU', 25 * '-', '\n')
        print('>>> Your country codes: ', list(self.__country_codes), '\n')
        print('1. Detailed analysis for each country separately')
        print('2. Detailed analysis for all countries together')
        print('0. Back')
        print('\n', 70 * '-', '\n')

    @staticmethod
    def __create_paragraph(title: str, text):
        return f"\n {20 * '-'} {str.upper(title)} {20 * '-'}\n\n{text}\n"

    @property
    def country_codes(self) -> set:
        return self.__country_codes

    @country_codes.setter
    def country_codes(self, value: set):
        self.__country_codes = value
