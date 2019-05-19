import os
from nltk.corpus import stopwords

from wordcloud import WordCloud, STOPWORDS

import numpy as np

import pandas as pd
from pandas import DataFrame

import seaborn as sns
import matplotlib.pyplot as plt

from util.args import Args


def __download_stopwords():
    # Collect all the related stopwords.

    all_stopwords = list(stopwords.words('english'))
    all_stopwords.extend(list(stopwords.words('german')))
    all_stopwords.extend(list(stopwords.words('french')))
    all_stopwords.extend(list(stopwords.words('russian')))

    all_stopwords.extend(['https', 'youtube', 'VIDEO', 'youtu', 'CHANNEL', 'WATCH'])

    return all_stopwords


USER_STOPWORDS = set(__download_stopwords())


def views_likes_dislikes_comments_normal_distribution(data: DataFrame, output_dir=Args.analysis_res_dir()):
    data['likes_log'] = np.log(data['likes'] + 1)
    data['view_count_log'] = np.log(data['view_count'] + 1)
    data['dislikes_log'] = np.log(data['dislikes'] + 1)
    data['comment_log'] = np.log(data['comment_count'] + 1)

    plt.figure(figsize=(12, 6))

    plt.subplot(221)
    g1 = sns.distplot(data['view_count_log'])
    g1.set_title("VIEWS LOG DISTRIBUTION", fontsize=16)

    plt.subplot(224)
    g2 = sns.distplot(data['likes_log'], color='green')
    g2.set_title('LIKES LOG DISTRIBUTION', fontsize=16)

    plt.subplot(223)
    g3 = sns.distplot(data['dislikes_log'], color='r')
    g3.set_title("DISLIKES LOG DISTRIBUTION", fontsize=16)

    plt.subplot(222)
    g4 = sns.distplot(data['comment_log'])
    g4.set_title("COMMENTS LOG DISTRIBUTION", fontsize=16)

    plt.subplots_adjust(wspace=0.2, hspace=0.4, top=0.9)

    __save_figure(plt, output_dir, 'normal_distribution.png')
    plt.close()


def correlation(data: DataFrame, output_dir=Args.analysis_res_dir()):
    corr = data[['view_count', 'likes', 'dislikes', 'comment_count']].corr()
    plot = sns.heatmap(corr, cmap='Blues', annot=True)

    __save_figure(plot.get_figure(), output_dir, 'correlation.png')
    plt.close()


def category_rating(data: DataFrame, output_dir=Args.analysis_res_dir()):
    plt.figure(figsize=(30, 9))
    plot = sns.countplot(data['category'], order=data['category'].value_counts().index)
    plot.set_title("Counting the Video Category's ", fontsize=20)
    plot.set_xlabel("", fontsize=20)
    plot.set_ylabel("Count", fontsize=20)

    __save_figure(plot.get_figure(), output_dir, 'category_rating.png')
    plt.close()


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
    plt.close()


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
    plt.close()


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
    plt.close()


# Top videos whose view_count grow fastest among categories
def view_count_fastest_grow_among_categories(data: DataFrame, preprocessing=True):
    if preprocessing:
        data = distribution_of_days_preprocessing(data)

    # calculate growth rate for each video
    data['growth_rate_view'] = data['view_count'] / (data['interval'] + 1)

    df = data.set_index(keys='title').groupby(by=['category'])['channel_title', 'growth_rate_view'].apply(
        lambda g: g.nlargest(5, 'growth_rate_view'))
    return df.head(90)


# Top videos whose likes grow fastest among categories
def likes_fastest_grow_among_categories(data: DataFrame, preprocessing=True):
    if preprocessing:
        data = distribution_of_days_preprocessing(data)

    # calculate growth rate for each video
    data['growth_rate_like'] = data['likes'] / (data['interval'] + 1)

    df = data.set_index(keys='title').groupby(by=['category'])['channel_title', 'growth_rate_like'].apply(
        lambda g: g.nlargest(5, 'growth_rate_like'))
    return df.head(90)


# Top videos whose dislikes grow fastest among categories
def dislikes_fastest_grow_among_categories(data: DataFrame, preprocessing=True):
    if preprocessing:
        data = distribution_of_days_preprocessing(data)

    # calculate growth rate for each video
    data['growth_rate_dislike'] = data['dislikes'] / (data['interval'] + 1)

    df = data.set_index(keys='title').groupby(by=['category'])['channel_title', 'growth_rate_dislike'].apply(
        lambda g: g.nlargest(5, 'growth_rate_dislike'))
    return df.head(90)


# Top videos whose comment_count grow fastest among categories
def comment_count_fastest_grow_among_categories(data: DataFrame, preprocessing=True):
    if preprocessing:
        data = distribution_of_days_preprocessing(data)

    # calculate growth rate for each video
    data['growth_rate_comment'] = data['comment_count'] / (data['interval'] + 1)

    df = data.set_index(keys='title').groupby(by=['category'])['channel_title', 'growth_rate_comment'].apply(
        lambda g: g.nlargest(5, 'growth_rate_comment'))
    return df.head(90)


def top_channels(data: DataFrame, num_of_channels: int):
    channel = pd.DataFrame(data['channel_title'].groupby(by=[data['channel_title'], data['category']]).count())
    channel.columns = ['count']
    top_channel = channel.nlargest(num_of_channels, ['count'])
    return top_channel.head(num_of_channels)


def word_cloud_for_tags(data: DataFrame, output_dir=Args.analysis_res_dir()):
    tags_word = data['tags'].str.lower().str.cat(sep=' ')

    # word_tokens = word_tokenize(tags_word)
    # filtered_sentence = [w for w in word_tokens if not w in all_stopwords]
    # without_single_chr = [word for word in filtered_sentence if len(word) > 2]
    # cleaned_data_title = [word for word in without_single_chr if not word.isdigit()]

    __create_and_save_word_cloud(
        data=tags_word,
        filename='word_cloud_for_tags.png',
        user_stopwords=USER_STOPWORDS,
        output_dir=output_dir
    )

    del tags_word


def word_cloud_for_titles(data: DataFrame, output_dir=Args.analysis_res_dir()):
    title_word = data['title'].str.lower().str.cat(sep=' ')

    # word_tokens = word_tokenize(title_word)
    # filtered_sentence = [w for w in word_tokens if not w in all_stopwords]
    # without_single_chr = [word for word in filtered_sentence if len(word) > 2]
    # cleaned_data_title = [word for word in without_single_chr if not word.isdigit()]

    __create_and_save_word_cloud(
        data=title_word,
        filename='word_cloud_for_titles.png',
        user_stopwords=USER_STOPWORDS,
        output_dir=output_dir
    )

    del title_word


def word_cloud_for_description(data: DataFrame, output_dir=Args.analysis_res_dir()):
    description_word = data['title'].str.lower().str.cat(sep=' ')

    # word_tokens = word_tokenize(description_word)
    # filtered_sentence = [w for w in word_tokens if not w in all_stopwords]
    # without_single_chr = [word for word in filtered_sentence if len(word) > 2]
    # cleaned_data_title = [word for word in without_single_chr if not word.isdigit()]

    __create_and_save_word_cloud(
        data=description_word,
        filename='word_cloud_for_description.png',
        user_stopwords=USER_STOPWORDS,
        output_dir=output_dir
    )

    del description_word


def __save_figure(figure, output_dir, filename):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    figure.savefig(os.path.join(output_dir, filename))


def __create_and_save_word_cloud(
        data,
        filename,
        output_dir=Args.analysis_res_dir(),
        user_stopwords=STOPWORDS,
        bg_color='black',
        max_words=100,
        max_font_size=120):
    plt.figure(figsize=(20, 20))
    cloud = WordCloud(
        stopwords=user_stopwords,
        background_color=bg_color,
        max_words=max_words,
        max_font_size=max_font_size,
        width=1600, height=800
    ).generate(data)

    plt.imshow(cloud)
    plt.axis('off')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.savefig(os.path.join(output_dir, filename), facecolor='k', bbox_inches='tight')
    plt.close()

# def sentiment_analysis(data: DataFrame, output_dir=Args.analysis_res_dir()):
#     category_list = data['category'].unique()
#
#     # Collect all the related stopwords.
#     en_stopwords = list(stopwords.words('english'))
#     de_stopwords = list(stopwords.words('german'))
#     fr_stopwords = list(stopwords.words('french'))
#     ru_stopwords = list(stopwords.words('russian'))
#
#     en_stopwords.extend(de_stopwords)
#     en_stopwords.extend(fr_stopwords)
#     en_stopwords.extend(ru_stopwords)
#
#     polarities = list()
#     MAX_N = 1000
#
#     for i in category_list:
#         tags_word = data[data['category'] == i]['tags'].str.lower().str.cat(sep=' ')
#
#         # removes punctuation,numbers and returns list of words
#         tags_word = re.sub('[^A-Za-z]+', ' ', tags_word)
#         word_tokens = word_tokenize(tags_word)
#         filtered_sentence = [w for w in word_tokens if not w in en_stopwords]
#         without_single_chr = [word for word in filtered_sentence if len(word) > 2]
#
#         # Remove numbers
#         cleaned_data_title = [word for word in without_single_chr if not word.isdigit()]
#
#         # Calculate frequency distribution
#         word_dist = nltk.FreqDist(cleaned_data_title)
#         hnhk = pd.DataFrame(word_dist.most_common(MAX_N),
#                             columns=['Word', 'Frequency'])
#         print(i)
#         compound = .0
#         for word in hnhk['Word'].head(MAX_N):
#             compound += SentimentIntensityAnalyzer().polarity_scores(word)['compound']
#
#         polarities.append(compound)
#
#     print(polarities)
