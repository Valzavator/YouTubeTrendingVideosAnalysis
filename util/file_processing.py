import pandas as pd
import os
import time

from util.args import Args
from util.string_processing import prepare_feature_for_csv


def get_data_from_file(file_path: str) -> list:
    with open(file_path) as file:
        lines = [line.strip() for line in file]

    return lines


def write_to_file(output_dir, file_name, data):
    if output_dir is None:
        raise NotADirectoryError('Invalid output directory name!')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, file_name), "w+",
              encoding='utf-8') as file:
        for row in data:
            file.write(f"{row}\n")


def get_videos_data_from_csv(*files) -> list:
    data_frames = []

    for file in files:
        try:
            if file is None:
                continue
            data_frames.append(pd.read_csv(file))
        except FileNotFoundError as e:
            print(e.strerror)

    if len(data_frames) == 0:
        return []

    videos_data = pd.concat(data_frames).to_dict('records')

    return videos_data


def save_videos_data_into_csv(
        videos_data: list,
        file_name=f"{time.strftime('%d-%m-%y_%H.%M.%S')}_videos.csv",
        output_dir=Args.raw_data_dir()):
    if videos_data is None:
        raise ValueError('Videos data can`t be None!')

    csv_data = [','.join(videos_data[0].keys())]

    for video in videos_data:
        if video is None:
            continue

        csv_data.append(','.join([prepare_feature_for_csv(val) for val in video.values()]))

    write_to_file(
        output_dir,
        file_name,
        csv_data)
