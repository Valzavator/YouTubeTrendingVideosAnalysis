import json

from util.args import Args
from util.file_processing import get_videos_data_from_csv, save_videos_data_into_csv


def match_category_id_with_category_title(videos_data: list, category_id_file_path=None) -> list:
    if videos_data is None:
        raise ValueError('Videos data can`t be None!')

    if category_id_file_path is None:
        category_id_file_path = Args.category_id_file_path()

    categories = {}
    with open(category_id_file_path, 'r') as f:
        category = json.load(f)
        for i in category['items']:
            categories[int(i['id'])] = i['snippet']['title']

    for video in videos_data:
        if 'category' not in video:
            category_id = video.pop('category_id')
            video['category'] = categories.get(int(category_id), category_id)

    return videos_data


def reformat_dataset(file_path: str, filename: str, country_code: str):
    if file_path is None:
        raise ValueError('File path can`t be None!')

    if country_code is None:
        raise ValueError('Country code can`t be None!')

    data = get_videos_data_from_csv(file_path)

    data = match_category_id_with_category_title(data)

    for video in data:
        video['_id'] = video['_id'] + video['trending_date']
        video.pop('video_error_or_removed')
        video['country_code'] = f'"{country_code}"'

    save_videos_data_into_csv(data, filename)
