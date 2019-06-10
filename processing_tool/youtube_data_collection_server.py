from datetime import datetime, date, time
import time as t

from database.database import Database
from processing_tool.data_preprocessing import match_category_id_with_category_title
from processing_tool.scraper import YouTubeTrendingVideosScraper
from util.args import Args
from util.file_processing import save_videos_data_into_csv


class YouTubeDataCollectionServer(object):

    def __init__(self):
        self.db = Database()
        self.scraper = YouTubeTrendingVideosScraper()

    def launch(self, hours=23, minutes=30, country_codes_path=Args.country_codes_path()):

        scrap_time = datetime.combine(date.today(), time(hours, minutes))

        while True:
            current_time = datetime.today()
            delta_time = (scrap_time - current_time)
            scrap_time = scrap_time.fromtimestamp(scrap_time.timestamp() + abs(delta_time.days) * 86400)

            print(f'>>> Next scrap will be {scrap_time.strftime("%Y.%m.%d-%H:%M:%S")}')

            t.sleep(delta_time.seconds)

            new_data = match_category_id_with_category_title(
                self.scraper.get_videos_data_by_country_codes_from_file(country_codes_path))

            print(f'>>> New {len(new_data)} data videos received!')

            count = self.db.save_many_videos(new_data)

            print(f'>>> Saved {count} data videos to database!')

            save_videos_data_into_csv(new_data)
