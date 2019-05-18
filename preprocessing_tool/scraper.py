import requests
import sys
import time

from entity.video import YouTubeVideo
from util.args import Args
from util.file_processing import get_data_from_file
from util.string_processing import prepare_feature, get_tags


class YouTubeTrendingVideosScraper:

    def __init__(self):

        self.__api_key = Args.api_key()

    def get_videos_data_by_country_codes(self, country_codes: list) -> list:
        countries_data = []

        for country_code in country_codes:
            countries_data = countries_data + self.__get_videos_data_by_country(country_code)

        return countries_data

    def get_videos_data_by_country_codes_from_file(self, file_path: str) -> list:
        country_codes = get_data_from_file(file_path)

        return self.get_videos_data_by_country_codes(country_codes)

    def __get_videos_data_by_country(self, country_code, next_page_token="&") -> list:
        videos_data_by_country = []

        # Because the API uses page tokens (which are literally just the same function of numbers everywhere) it is much
        # more inconvenient to iterate over pages, but that is what is done here.
        while next_page_token is not None:
            # A page of data i.e. a list of videos and all needed data
            video_data_page = self.__api_request(next_page_token, country_code)
            # Get the next page token and build a string which can be injected into the request with it, unless it's
            # None, then let the whole thing be None so that the loop ends after this cycle
            next_page_token = video_data_page.get("nextPageToken", None)
            next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token

            # Get all of the items as a list and let get_videos return the needed features
            items = video_data_page.get('items', [])

            videos_data_by_country += self.__get_videos_data_by_page(items, country_code)

        return videos_data_by_country

    def __api_request(self, page_token, country_code):
        # Builds the URL and requests the JSON from it
        request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet{page_token}" \
            f"chart=mostPopular&regionCode={country_code}&maxResults=50&key={self.__api_key}"
        request = requests.get(request_url)
        if request.status_code == 429:
            print("Temp-Banned due to excess requests, please wait and continue later...")
            sys.exit()

        return request.json()

    def __get_videos_data_by_page(self, items: list, country_code: str) -> list:
        videos_data_by_page = []

        for video_raw_data in items:

            video = YouTubeVideo()

            # We can assume something is wrong with the video if it has no statistics,
            #  often this means it has been deleted so we can just skip it
            if "statistics" not in video_raw_data:
                continue

            video.country_code = country_code

            # Snippet and statistics are sub-dicts of video, containing the most useful info
            snippet = video_raw_data['snippet']
            statistics = video_raw_data['statistics']

            # All features in snippet that are 1 deep and require no special processing

            video.title = prepare_feature(snippet.get("title", ""))
            video.published_at = prepare_feature(snippet.get("publishedAt", ""))
            video.channel_title = prepare_feature(snippet.get("channelTitle", ""))
            video.category_id = prepare_feature(snippet.get("categoryId", ""))

            # The following are special case features which require unique processing,
            # or are not within the snippet dict
            video.description = snippet.get("description", "")
            video.thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
            video.trending_date = time.strftime("%y.%d.%m")
            video.tags = get_tags(snippet.get("tags", "[none]"))
            video.view_count = statistics.get("viewCount", 0)

            # This may be unclear, essentially the way the API works is that if a video has comments or ratings disabled
            # then it has no feature for it, thus if they don't exist in the statistics dict we know they are disabled
            if 'likeCount' in statistics and 'dislikeCount' in statistics:
                video.likes = statistics['likeCount']
                video.dislikes = statistics['dislikeCount']
                video.ratings_disabled = False

            if 'commentCount' in statistics:
                video.comment_count = statistics['commentCount']
                video.comments_disabled = False

            video._id = prepare_feature(video_raw_data['id'] + video.trending_date)

            videos_data_by_page.append(video.__dict__)

        return videos_data_by_page
