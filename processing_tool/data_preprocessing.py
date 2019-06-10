import json

from util.args import Args


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


def reformat_dataset(data: list, country_code: str) -> list:
    if country_code is None:
        raise ValueError('Country code can`t be None!')

    data = match_category_id_with_category_title(data)

    for video in data:
        video['_id'] = video['_id'] + video['trending_date'] + country_code
        video.pop('video_error_or_removed')
        video['country_code'] = f'"{country_code}"'

    return data


def get_tags(tags_list):
    # Takes a list of tags, prepares each tag and joins them into a string by the pipe character
    return prepare_feature("|".join(tags_list))


def remove_unsafe_characters(string: str, unsafe_characters=None) -> str:
    # Any characters to exclude, generally these are things that become problematic in CSV files
    if unsafe_characters is None:
        unsafe_characters = ['\n', '"']

    # Removes any character from the unsafe characters list and surrounds the whole item in quotes
    for ch in unsafe_characters:
        string = str(string).replace(ch, '')

    return string


def prepare_feature(feature: str) -> str:
    feature = remove_unsafe_characters(feature)

    return f'{feature}'


def prepare_feature_for_csv(feature: str) -> str:
    feature = remove_unsafe_characters(feature)

    return f'"{feature}"'
