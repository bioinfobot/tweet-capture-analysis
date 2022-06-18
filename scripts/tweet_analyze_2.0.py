# Standard library.
import sys


# External library.
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist


# bioinforbot imports
sys.path.append(".")
import bioinfobot.utils.tweet_utils as t_utils
import bioinfobot.utils.datatype_utils as d_utils
from bioinfobot.utils.collector import get_latest_tweet_data

nltk.download("punkt")
nltk.download("stopwords")


# getting the latest tweet data file (json file)
data_path = get_latest_tweet_data()
print(f"Loading data from {data_path}")
tweet_df = pd.read_csv(data_path, sep="\t")

# setting up file name
date_info = tweet_df["Date"][0].split("-")
month, year = date_info[1], date_info[0]
name = f"{year}-{month}"

# extracting data
print("Extracting tweets")
total_hash = t_utils.extract_hash(tweet_df["Text"].tolist())

# data Preprocessing
tweet_df["Text"] = tweet_df["Text"].apply(t_utils.tweet_clean)
tweet_df["Tokens"] = tweet_df["Text"].apply(word_tokenize)
tweet_df["Tokens"] = tweet_df["Tokens"].apply(t_utils.filter_tokens)
word_tokens = d_utils.flatten_list(tweet_df["Tokens"].tolist())

# data collections
print("Analyzing Tweets")
n_rows = len(tweet_df)
n_words = len(word_tokens)
total_lang = t_utils.count_prog_langs(total_hash)

# measuring frequencies
freq = FreqDist(word_tokens)
n_unique_words = len(freq)
hash_freq = FreqDist(total_hash)
user_freq = FreqDist(tweet_df["ScreenName"].tolist())
lang_freq = FreqDist(total_lang)

top_words = d_utils.dict_value_sort_return_top(freq, 20)
hash_freq_sorted = d_utils.dict_value_sort_return_top(hash_freq, 20)
lang_freq_sorted = d_utils.dict_value_sort_return_top(lang_freq, 20)
users_freq_sorted = d_utils.dict_value_sort_return_top(user_freq, 20)

non_zero_lang = []
for i in range(len(lang_freq_sorted)):
    if lang_freq_sorted[i][1] > 0:
        non_zero_lang.append(lang_freq_sorted[i])

# generated word cloud
print("Generating word cloud")
t_utils.create_wordcloud(name, freq)

# json file
print("Saving analyized tweets into json file")
t_utils.create_json(
    name,
    top_words,
    n_rows,
    n_words,
    n_unique_words,
    hash_freq_sorted,
    users_freq_sorted,
    non_zero_lang,
)
