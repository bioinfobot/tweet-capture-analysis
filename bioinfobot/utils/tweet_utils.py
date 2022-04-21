"""
DESCRIPTION     : Custom function library.
USAGE           : from twitterfunc import tweet_clean
OUTPUT          : function return
AUTHOR          : Dr. Rohit Farmer
EMAIL           : rohit.farmer@gmail.com
"""
import os
import re
import string
import json

import pandas as pd
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk import FreqDist
from wordcloud import WordCloud

# bioinforbot imports
from bioinfobot.utils.paths import TweetAnalysisPaths


def tweet_clean(text):
    """Function to remove unwanted text/words from tweets. This is independent of nltk stopwords method."""
    # Remove hyperlinks
    text = re.sub("https://\S+", "", text)
    text = re.sub("http://\S+", "", text)
    # Remove &
    text = re.sub("&amp", "", text)
    # Remove hashtags
    text = re.sub("#\w+", "", text)
    text = re.sub("#", " ", text)
    # Remove citations
    text = re.sub("@\w+", "", text)
    # Remove tickers
    text = re.sub("\$\w+", "", text)
    # Remove punctuation
    text = re.sub("[" + string.punctuation + "]+", "", text)
    # # Remove quotes
    text = re.sub("&*[amp]*;|gt+", "", text)
    # Remove RT and CT
    text = re.sub("rt\s+", "", text)
    text = re.sub("ct\s+", "", text)
    # Remove linebreak, tab, return
    text = re.sub("[\n\t\r]+", "", text)
    # Remove via with blank
    text = re.sub("via+\s", "", text)
    # Remove multiple whitespace
    text = re.sub("\s+\s+", " ", text)
    # Remove anything that is not a unicode character
    text = re.sub("\W", " ", text)
    # Remove digits
    text = re.sub("\d+", "", text)
    return text


def extract_hash(tweets):
    """extracts all hastags in tweets

    Parameters
    ----------
    tweet : list
        list of all tweets

    Returns
    -------
    list
        list of hastags found in tweets

    Raises
    ------
    TypeError
        Raised if tweets is not a list
    """
    # type checking
    if not isinstance(tweets, list):
        raise TypeError("tweets must be a list")

    total_hash = []
    for tweet in tweets:
        hash_match = re.findall("#\w+", tweet.lower())
        if not hash_match:
            continue
        else:
            total_hash += hash_match

    total_hash = filter_hash(total_hash)
    return total_hash


def filter_hash(hashes):
    """Removes unwanted hashtags

    Parameters
    ----------
    hashes : list
        list of all hastags
    """
    # type checking
    if not isinstance(hashes, list):
        raise TypeError("hashes must be a list")

    # TODO: Create a class that contains all stop words
    stop_hash = ["#twitter", "#tweeted"]
    filtered_hash = [hashtag for hashtag in hashes if hashtag not in stop_hash]
    return filtered_hash


def create_wordcloud(name: str, words_freq: dict) -> None:
    """Generates word cloud image and saved int the images/ folder

    Parameters
    ----------
    name : str
        name

    words_freq : dict
        dictionary containing unique words and its associated frequency
        as key value pairs

    Returns
    -------
        None
    """
    # instantiating paths
    paths = TweetAnalysisPaths()

    font_style = os.path.join(paths.font_path, "Actor-Regular.ttf")
    image_path = f"{paths.images_path}/{name}.png"

    # word cloud parameters
    wordcloud = WordCloud(
        font_path=font_style,
        width=1500,
        height=500,
        max_words=500,
        stopwords=None,
        background_color="whitesmoke",
        max_font_size=None,
        font_step=1,
        mode="RGB",
        collocations=True,
        colormap=None,
        normalize_plurals=True,
    ).generate_from_frequencies(words_freq)

    wordcloud.to_file(image_path)


# Tweet data utils
def filter_tokens(words):
    nltk_stopwords = list(stopwords.words("english"))
    # TODO: Might this called as a seperate class or struct?
    more_stopwords = [
        "also",
        "bad",
        "cant",
        "could",
        "dont",
        "day",
        "great",
        "get",
        "good",
        "hear",
        "here",
        "ive",
        "im",
        "like",
        "latest",
        "new",
        "news",
        "oh",
        "people",
        "see",
        "today",
        "top",
        "the",
        "twitter",
        "thats",
        "thanks",
        "us",
        "using",
        "work",
        "would",
        "x",
    ]
    stop_words = nltk_stopwords + more_stopwords
    filtered_tokens = [word for word in words if word not in stop_words]
    return filtered_tokens


def extract_hash(tweets):
    """extracts all hastags in tweets

    Parameters
    ----------
    tweet : list
        list of all tweets

    Returns
    -------
    list
        list of hastags found in tweets

    Raises
    ------
    TypeError
        Raised if tweets is not a list
    """
    # type checking
    if not isinstance(tweets, list):
        raise TypeError("tweets must be a list")

    total_hash = []
    for tweet in tweets:
        hash_match = re.findall("#\w+", tweet.lower())
        if not hash_match:
            continue
        else:
            total_hash += hash_match

    total_hash = filter_hash(total_hash)
    return total_hash


def filter_hash(hashes):
    """Removes unwanted hashtags

    Parameters
    ----------
    hashes : list
        list of all hastags
    """
    # type checking
    if not isinstance(hashes, list):
        raise TypeError("hashes must be a list")

    # TODO: Create a class that contains all stop words
    stop_hash = ["#twitter", "#tweeted"]
    filtered_hash = [hashtag for hashtag in hashes if hashtag not in stop_hash]
    return filtered_hash


def create_wordcloud(name: str, words_freq: dict) -> None:
    """Generates word cloud image and saved int the images/ folder

    Parameters
    ----------
    name : str
        name

    words_freq : dict
        dictionary containing unique words and its associated frequency
        as key value pairs

    Returns
    -------
        None
    """
    # instantiating paths
    paths = TweetAnalysisPaths()

    font_style = os.path.join(paths.font_path, "Actor-Regular.ttf")
    image_path = f"{paths.images_path}/{name}.png"

    # word cloud parameters
    wordcloud = WordCloud(
        font_path=font_style,
        width=1500,
        height=500,
        max_words=500,
        stopwords=None,
        background_color="whitesmoke",
        max_font_size=None,
        font_step=1,
        mode="RGB",
        collocations=True,
        colormap=None,
        normalize_plurals=True,
    ).generate_from_frequencies(words_freq)

    wordcloud.to_file(image_path)


def create_json(
    name,
    top_words,
    row_count,
    total_words,
    unique_word,
    hash_freq_sorted,
    users_freq_sorted,
    lang_nonzero,
):
    """_summary_

    Parameters
    ----------
    name : str
        name of the outfile
    top_words : list
        list of top words
    row_count : int
        number of entries
    total_words : int
        total amount of words
    unique_word : list
        list of unique words
    hash_freq_sorted : dict
        dictionary containing hash words and counts as key value pairs
    users_freq_sorted : dict
        dictionary containing user names and tweet counts as key value pairs
    lang_nonzero : list
        list of tuples containing (lang_name, counts) in each tuple

    Returns
    -------
    None
        Generates a JSON file saved into the data/ folder
    """

    main_dump = {
        "TopWords": top_words,
        "TweetCount": row_count,
        "TotalWords": total_words,
        "UniqueWords": unique_word,
        "HashFreq": hash_freq_sorted,
        "UsersFreq": users_freq_sorted,
        "PopularLanguages": lang_nonzero,
    }

    json_path = f"../data/{name}.json"
    with open(json_path, "w") as outfile:
        json.dump(main_dump, outfile)

    return json_path


def count_prog_langs(hash_list):
    """_summary_

    Parameters
    ----------
    hash_list : list
       list containing all collected hash tag words

    Returns
    -------
    dict
        program langauge and counts as key value pairs
    """
    with open("../configs/programminglang.txt", "r") as progfile:
        # creating a dictionary of all langauges with a count of zerio
        loaded_langs = set([prog_name.rstrip() for prog_name in progfile])

    # iterate through all hashes and counting languages
    found_langs = []
    for hash in hash_list:
        for prog_lang in loaded_langs:
            search = f"#{prog_lang.lower()}"
            if search in hash:
                found_langs.append(prog_lang)

    return found_langs
