from io import UnsupportedOperation
import os

class TweetAnalysisPaths():
    """ Object containing paths in the tweet analysis folder"""
    def __init__(self):
        root_dir = self.__set_root()
        self.root_path = root_dir
        self.data_path = os.path.join(self.root_path, "data")
        self.images_path = os.path.join(self.root_path, "images")
        self.tweet_data = os.path.join(self.data_path, "tweet_data")

    def __set_root(self):
        full_path = os.getcwd()
        root_name = "bioinfobot/tweet-capture-analysis"
        root_header = full_path.split(root_name)[0]
        root_path = os.path.join(root_header, root_name)
        return root_path

class WebSitePath():
    def __init__(self):
        raise NotImplementedError("Website path is not implemented yet")
        os.path
        self.image_path = ""