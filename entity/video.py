import time


class YouTubeVideo:

    def __init__(self):
        self._id = ""
        self.country_code = ""
        self.title = ""
        self.published_at = ""
        self.channel_title = ""
        self.category_id = ""
        self.trending_date = time.strftime("%y.%d.%m")
        self.tags = "[none]"
        self.view_count = 0
        self.likes = 0
        self.dislikes = 0
        self.comment_count = 0
        self.thumbnail_link = ""
        self.comments_disabled = True
        self.ratings_disabled = True
        self.description = ""
