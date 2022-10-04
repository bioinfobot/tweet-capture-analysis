import os
import logging


class TweetAnalysisPaths:
    """Object containing paths in the tweet analysis folder"""

    def __init__(self):

        # setting root path
        self.root_name = None
        self.root_path = None
        self.__set_root()

        # top level directories
        self.images_path = os.path.join(self.root_path, "images")
        self.data_path = os.path.join(self.root_path, "data")
        self.config_path = os.path.join(self.root_path, "configs")
        self.log_path = os.path.join(self.root_path, "logs")

        # containing files
        self.proglang_file = os.path.join(self.config_path, "programminglang.txt")
        self.tweet_data = os.path.join(self.data_path, "tweet_data")
        self.font_path = os.path.join(self.config_path, "fonts")

        # log files
        self.analysis_log = os.path.join(self.log_path, "tweet_analysis.logs")

    def __set_root(self):
        full_path = os.getcwd()
        root_name = "bioinfobot/tweet-capture-analysis"
        root_header = full_path.split(root_name)[0]
        root_path = os.path.join(root_header, root_name)

        if not os.path.exists(root_path):
            print(root_path)
            raise FileNotFoundError("unable to find `tweet-capture-analysis` path")

        self.root_name = root_name
        self.root_path = root_path


class WebsitePaths:
    def __init__(self):

        # setting root path
        self.root_name = None
        self.root_path = None
        self.__set_root()

        # paths
        self.website_wordcloud = os.path.join(self.root_path, "static/images/wordcloud")
        self.website_posts = os.path.join(self.root_path, "content/en/posts")

    def __set_root(self):
        current_path = os.getcwd()
        root_name = "bioinfobot/website-code/Bioinfobot"
        splitter = "bioinfobot/tweet-capture-analysis"
        root_header = current_path.split(splitter)[0]
        root_path = os.path.join(root_header, root_name)

        # check if it exists
        if not os.path.exists(root_path):
            raise FileNotFoundError("unable to find `website-code` path")

        self.root_name = root_name
        self.root_path = root_path
