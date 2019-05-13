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


def prepare_feature(feature: str, unsafe_characters=None) -> str:
    feature = remove_unsafe_characters(feature)

    return f'{feature}'


def prepare_feature_for_csv(feature: str, unsafe_characters=None) -> str:
    feature = remove_unsafe_characters(feature)

    return f'"{feature}"'
