import os

import pandas as pd
import numpy as np
import seaborn as sns
from pandas import DataFrame
import matplotlib.pyplot as plt

from util.args import Args


def correlation(data: DataFrame, output_dir=Args.analysis_res_dir()):
    corr = data[['view_count', 'likes', 'dislikes', 'comment_count']].corr()
    plot = sns.heatmap(corr, cmap='Blues', annot=True)

    __save_figure(plot.get_figure(), output_dir, 'correlation.png')


def category_rating(data: DataFrame, output_dir=Args.analysis_res_dir()):
    plt.figure(figsize=(30, 9))
    plot = sns.countplot(data['category'], order=data['category'].value_counts().index)
    plot.set_title("Counting the Video Category's ", fontsize=20)
    plot.set_xlabel("", fontsize=20)
    plot.set_ylabel("Count", fontsize=20)

    __save_figure(plot.get_figure(), output_dir, 'category_rating.png')


# Plot the distribution of 'view_count','likes','dislikes','comment_count'
def distribution_boxplot(data: DataFrame, output_dir=Args.analysis_res_dir()):
    view_count = np.log(data['view_count'] + 1)
    likes = np.log(data['likes'] + 1)
    dislikes = np.log(data['dislikes'] + 1)
    comment = np.log(data['comment_count'] + 1)

    data_count = pd.concat([view_count, likes, dislikes, comment], axis=1)
    data_count.index = data['category']
    data_count = data_count[(data_count != 0)]

    plt.figure(figsize=(32, 20))
    plt.subplot(2, 2, 1)
    sns.boxplot(data_count.index, 'view_count', data=data_count, order=data['category'].value_counts().index)
    plt.xticks(rotation=30, fontsize=12)

    plt.subplot(2, 2, 2)
    sns.boxplot(data_count.index, 'likes', data=data_count, order=data['category'].value_counts().index)
    plt.xticks(rotation=30, fontsize=12)

    plt.subplot(2, 2, 3)
    sns.boxplot(data_count.index, 'dislikes', data=data_count, order=data['category'].value_counts().index)
    plt.xticks(rotation=30, fontsize=12)

    plt.subplot(2, 2, 4)
    sns.boxplot(data_count.index, 'comment_count', data=data_count, order=data['category'].value_counts().index)
    plt.xticks(rotation=30, fontsize=12)

    __save_figure(plt, output_dir, 'distribution_boxplot.png')


# Plot the distribution of 'view_count','likes','dislikes','comment_count'
def distribution_plot(data: DataFrame, output_dir=Args.analysis_res_dir()):
    general_view = pd.DataFrame(
        data[['view_count', 'likes', 'dislikes', 'comment_count']].groupby(data['category']).mean())

    plt.figure(figsize=(32, 20))

    plt.subplot(2, 2, 1)
    plt.plot(general_view.index, 'view_count', data=general_view, color='blue', linewidth=2, linestyle='solid')
    plt.title('View_count vs Category')
    plt.xticks(rotation=30)

    plt.subplot(2, 2, 2)
    plt.plot(general_view.index, 'likes', data=general_view, color='green', linewidth=2, linestyle='dotted')
    plt.title('Likes vs Category')
    plt.xticks(rotation=30)

    plt.subplot(2, 2, 3)
    plt.plot(general_view.index, 'dislikes', data=general_view, color='black', linewidth=2, linestyle='dashed')
    plt.title('Dislikes vs Category')
    plt.xticks(rotation=30)

    plt.subplot(2, 2, 4)
    plt.plot(general_view.index, 'comment_count', data=general_view, color='red', linewidth=2, linestyle='dashdot')
    plt.title('Comment_count vs Category')
    plt.xticks(rotation=30)

    __save_figure(plt, output_dir, 'distribution_plot.png')


# The distribution of days that videos take to become popular
def distribution_of_days_preprocessing(data: DataFrame):
    data['published_at'] = pd.to_datetime(data['published_at'], errors='coerce', format='%Y-%m-%dT%H:%M:%S.%fZ')
    data['trending_date'] = pd.to_datetime(data['trending_date'], errors='coerce', format='%y.%d.%m')

    data['publish_date'] = data['published_at'].dt.date
    data['publish_time'] = data['published_at'].dt.time
    data['interval'] = (data['trending_date'].dt.date - data['publish_date']).astype('timedelta64[D]')

    return data


# Histogram of distribution of interval
def distribution_of_days(data: DataFrame, output_dir=Args.analysis_res_dir()):
    data = distribution_of_days_preprocessing(data)

    plt.figure(figsize=(25, 9))
    plot = sns.countplot(data['interval'])

    __save_figure(plot.get_figure(), output_dir, 'distribution_of_days.png')


# Top videos who view_count/likes grow fastest among categories
def fastest_grow_among_categories(data: DataFrame):
    data = distribution_of_days_preprocessing(data)

    # calculate growth rate for each video
    data['growth_rate_view'] = data['view_count'] / (data['interval'] + 1)
    data['growth_rate_like'] = data['likes'] / (data['interval'] + 1)
    data['growth_rate_dislike'] = data['dislikes'] / (data['interval'] + 1)
    data['growth_rate_comment'] = data['comment_count'] / (data['interval'] + 1)

    df = data.set_index(keys='title').groupby(by=['category'])['channel_title', 'growth_rate_view'].apply(
        lambda g: g.nlargest(10, 'growth_rate_view'))
    print(df.head(40))


def top_channels(data: DataFrame, num_of_channels: int):
    channel = pd.DataFrame(data['channel_title'].groupby(by=[data['channel_title'], data['category']]).count())
    channel.columns = ['count']
    top_channel = channel.nlargest(num_of_channels, ['count'])
    print(top_channel.head(num_of_channels))


def __save_figure(figure, output_dir, filename):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    figure.savefig(os.path.join(output_dir, filename))
