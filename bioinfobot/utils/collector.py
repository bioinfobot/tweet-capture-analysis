#--------------------------------------------------
# Module focuses on gathering data from the tweet_data
# directory
#--------------------------------------------------
import os
import glob

# bioinfobot imports
from bioinfobot.structs.paths import TweetAnalysisPaths


def select_tweet_dir_by_year(year: int) -> list:
    """Obtains all tweet data directory on given year

    Parameters
    ----------
    year : int

    Returns
    -------
    str
        path to tweet data of given year
    """
    paths = TweetAnalysisPaths()
    path = f"{paths.tweet_data}/{year}"
    if not os.path.exists(path):
        raise ValueError(f"Could not find tweet data for year {year}")
    return path


def get_latest_tweetdata_dir() -> str:
    """Obtainst the latest directory

    Returns
    -------
    str
        path to the latest tweet data directory
    """

    # get all directories base names
    paths = TweetAnalysisPaths()
    years = [int(os.path.basename(path)) for path in get_all_tweet_dirs()]
    latest_year = max(years)
    path = f"{paths.tweet_data}/{latest_year}"
    return path


def get_all_tweet_dirs() -> list:
    """Gets all tweet directories in `tweet_data` folder

    Returns
    -------
    list of all tweet_data directories
    """
    paths = TweetAnalysisPaths()
    all_dirs = glob.glob(f"{paths.tweet_data}/*")
    return all_dirs


def get_latest_tweet_data() -> str:
    """Obtains the latest collected tweet data

    Returns
    -------
    str
        Path to latest tweet data
    """
    latest_dir = get_latest_tweetdata_dir()
    month_paths = glob.glob(f"{latest_dir}/*")
    month_files = [os.path.basename(paths) for paths in month_paths]
    months = [int(month.split(".")[0]) for month in month_files]
    top_month = max(months)
    header_path = month_paths[0].rsplit("/", 1)[0]
    file_path = f"{header_path}/{top_month}.tsv"
    if not os.path.exists(file_path):
        raise FileNotFoundError()
    return file_path
