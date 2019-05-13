import time


class YouTubeVideo:

    def __init__(self):
        self._id = ""
        self.country_code = ""
        self.title = ""
        self.publishedAt = ""
        self.channelTitle = ""
        self.categoryId = ""
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
    #
    # @property
    # def video_id(self) -> str:
    #     return self.__video_id
    #
    # @video_id.setter
    # def video_id(self, value: str):
    #     self.__video_id = value
    #
    # @property
    # def title(self) -> str:
    #     return self.__title
    #
    # @title.setter
    # def title(self, value: str):
    #     self.__title = value
    #
    # @property
    # def publishedAt(self) -> str:
    #     return self.__publishedAt
    #
    # @publishedAt.setter
    # def publishedAt(self, value: str):
    #     self.__publishedAt = value
    #
    # @property
    # def channelId(self) -> str:
    #     return self.__channelId
    #
    # @channelId.setter
    # def channelId(self, value: str):
    #     self.__channelId = value
    #
    # @property
    # def channelTitle(self) -> str:
    #     return self.__channelTitle
    #
    # @channelTitle.setter
    # def channelTitle(self, value: str):
    #     self.__channelTitle = value
    #
    # @property
    # def categoryId(self) -> str:
    #     return self.__categoryId
    #
    # @categoryId.setter
    # def categoryId(self, value: str):
    #     self.__categoryId = value
    #
    # @property
    # def trending_date(self) -> str:
    #     return self.__trending_date
    #
    # @trending_date.setter
    # def trending_date(self, value: str):
    #     self.__trending_date = value
    #
    # @property
    # def tags(self) -> str:
    #     return self.__tags
    #
    # @tags.setter
    # def tags(self, value: str):
    #     self.__tags = value
    #
    # @property
    # def view_count(self) -> str:
    #     return self.__view_count
    #
    # @view_count.setter
    # def view_count(self, value: str):
    #     self.__view_count = value
    #
    # @property
    # def likes(self) -> str:
    #     return self.__likes
    #
    # @likes.setter
    # def likes(self, value: str):
    #     self.__likes = value
    #
    # @property
    # def dislikes(self) -> str:
    #     return self.__dislikes
    #
    # @dislikes.setter
    # def dislikes(self, value: str):
    #     self.__dislikes = value
    #
    # @property
    # def comment_count(self) -> str:
    #     return self.__comment_count
    #
    # @comment_count.setter
    # def comment_count(self, value: str):
    #     self.__comment_count = value
    #
    # @property
    # def thumbnail_link(self) -> str:
    #     return self.__thumbnail_link
    #
    # @thumbnail_link.setter
    # def thumbnail_link(self, value: str):
    #     self.__thumbnail_link = value
    #
    # @property
    # def comments_disabled(self) -> str:
    #     return self.__comments_disabled
    #
    # @comments_disabled.setter
    # def comments_disabled(self, value: str):
    #     self.__comments_disabled = value
    #
    # @property
    # def ratings_disabled(self) -> str:
    #     return self.__ratings_disabled
    #
    # @ratings_disabled.setter
    # def ratings_disabled(self, value: str):
    #     self.__ratings_disabled = value
    #
    # @property
    # def description(self) -> str:
    #     return self.__description
    #
    # @description.setter
    # def description(self, value: str):
    #     self.__description = value