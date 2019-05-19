# import os
#
# # import numpy as np
# # import pandas as pd
# # import seaborn as sns
# # import matplotlib.pyplot as plt
# # from database.database import Database
# # import pycountry
#
# # from entity.video import YouTubeVideo
# # from preprocessing_tool.data_processing import match_category_id_with_category_title, reformat_dataset
# import time
# from util.args import Args#
# # from util.file_processing import save_videos_data_into_csv, get_videos_data_from_csv
# from processing_tool.data_analysis import correlation
# from processing_tool.data_preprocessing import reformat_dataset
# from util.string_processing import prepare_feature
# from processing_tool.scraper import YouTubeTrendingVideosScraper
# from util.file_processing import get_videos_data_from_csv
import nltk

# nltk.download()

if __name__ == "__main__":
    pass




    # output_directory = f'{Args.analysis_res_dir()}\\all_country\\{time.strftime("%d.%m.%y")}\\'
    # db = Database()
    # scraper = YouTubeTrendingVideosScraper()
    # data = scraper.get_videos_data_by_country_codes({'UA', 'US'})
    #
    # print(data)
    # match_category_id_with_category_title(data)
    # save_videos_data_into_csv(data)
    # for video in scraper.get_videos_data_by_country_codes(['UA']):
    #     print(video.__dict__)
    # data = db.get_videos_by_countries(['US', 'CA', 'DE', 'FR', 'GB', 'IN'])
    # print(len(data))
    # data = match_category_id_with_category_title(data)
    #
    # reformat_dataset('resource/raw_data/USvideos.csv', 'US_videos.csv', 'US')
    # reformat_dataset('resource/raw_data/CAvideos.csv', 'CA_videos.csv', 'CA')
    # reformat_dataset('resource/raw_data/DEvideos.csv', 'DE_videos.csv', 'DE')
    # reformat_dataset('resource/raw_data/FRvideos.csv', 'FR_videos.csv', 'FR')
    # reformat_dataset('resource/raw_data/GBvideos.csv', 'GB_videos.csv', 'GB')
    # reformat_dataset('resource/raw_data/INvideos.csv', 'IN_videos.csv', 'IN')

    # data = get_videos_data_from_csv(
    #     'resource/raw_data/CA_videos.csv',
    #     'resource/raw_data/DE_videos.csv',
    #     'resource/raw_data/FR_videos.csv',
    #     'resource/raw_data/GB_videos.csv',
    #     'resource/raw_data/IN_videos.csv',
    #     'resource/raw_data/US_videos.csv',
    # )
    #
    # data = get_videos_data_from_csv(
    #     'resource/raw_data/US_videos.csv',
    # )
    #
    # print(len(data))
    #
    # for d in data:
    #     db.save_one_video(d)

    # print(db.save_many_videos(data))

    # print(len(db.get_videos()))

###############
# dataset = get_videos_data_from_csv(
#     'resource/raw_data/US_videos.csv',
# )
#
    # df = pd.DataFrame(data)
    # print(df.head(5).to_string())
    # df.info()
    # df[['view_count','likes','dislikes','comment_count']].describe()
    # #
    # print(df.loc[(df['view_count'] == 0) | (df['likes'] == 0) | (df['dislikes'] == 0) | (
    #             df['comment_count'] == 0)].head().to_string())
    #
    # correlation(df)
    #
    # plt.figure(figsize=(25, 9))
    # plot = sns.countplot(data['category'], order=data['category'].value_counts().index)
    # figure = plot.get_figure()
    # figure.savefig('2.png')
