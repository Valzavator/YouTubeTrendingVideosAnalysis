import numpy as np
import pandas as pd
import json

import seaborn as sns
import matplotlib.pyplot as plt

from database.database import Database
from entity.video import YouTubeVideo
from preprocessing_tool.data_processing import match_category_id_with_category_title, reformat_dataset
from preprocessing_tool.scraper import YouTubeTrendingVideosScraper
from util.args import Args

from util.file_processing import save_videos_data_into_csv, get_videos_data_from_csv
from util.string_processing import prepare_feature

if __name__ == "__main__":
    # scraper = YouTubeTrendingVideosScraper()
    # data = scraper.get_videos_data_by_country_codes(['UA'])

    # match_category_id_with_category_title(data)
    # save_videos_data_into_csv(data)
    # for video in scraper.get_videos_data_by_country_codes(['UA']):
    #     print(video.__dict__)
    db = Database()
    print(len(db.get_videos_by_countries(['UA', 'US', 'CA', 'DE', 'FR', 'GB', 'IN'])))
    # data = match_category_id_with_category_title(data)

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
    # print(len(data))
    # print(db.save_many_videos(data))
    #
    # print(len(db.get_videos()))

###############
# dataset = get_videos_data_from_csv(
#     'resource/raw_data/US_videos.csv',
# )
#
# data = pd.DataFrame(dataset)

# data.info()
# data[['view_count','likes','dislikes','comment_count']].describe()

# print(data.loc[(data['view_count'] == 0) | (data['likes'] == 0) | (data['dislikes'] == 0) | (
#             data['comment_count'] == 0)].head().to_string())

# correlation = data[['view_count', 'likes', 'dislikes', 'comment_count']].corr()
# plot = sns.heatmap(correlation, cmap='Blues', annot=True)
# figure = plot.get_figure()
# figure.savefig('1.png')

# plt.figure(figsize=(25, 9))
# plot = sns.countplot(data['category'], order=data['category'].value_counts().index)
# figure = plot.get_figure()
# figure.savefig('2.png')
