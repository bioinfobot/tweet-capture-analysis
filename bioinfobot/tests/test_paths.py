import os
import unittest
from pathlib import Path
import logging

# bioinfobot imports
from bioinfobot.structs.paths import TweetAnalysisPaths

class TestPaths(unittest.TestCase):

    # NOTE: this allow to print outputs while testing
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    def test_paths(self):
        """ Checks if the path class is able to find root folder"""
        p = TweetAnalysisPaths()
        home_path = Path.home()
        root_path = os.path.join(home_path, "Projects/bioinfobot/tweet-capture-analysis")
        data_path = os.path.join(root_path, "data")
        img_path = os.path.join(root_path, "images")

        self.assertEqual(root_path, p.root_path)
        self.assertEqual(data_path, p.data_path)
        self.assertEqual(img_path, p.image_path)

if __name__ == "__main__":
    unittest.main()