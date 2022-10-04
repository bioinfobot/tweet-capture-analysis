import os
import argparse
import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd

# bioinfobot imports
from bioinfobot.structs.paths import TweetAnalysisPaths


def get_year(datetime):
    """parses date time string and return the year

    Parameters
    ----------
    datetime : str
        string containing date time data

    Return
    ------
    str
        year string
    """
    year_string = datetime.split("-")[0]
    return year_string


def get_month(datetime):
    """parses

    Parameters
    ----------
    datetime : str
        string containing date and time data

    Return
    ------
    str
        month string
    """
    month_string = datetime.split("-")[1]
    return month_string


def load_as_dataframe(db_path):
    """Loads database file and converts into pandas dataframe

    Parameters
    ----------
    db_path : str
        path to string database

    Returns
    -------
    pd.DataFrame
        pandas dataframe containing all tweet data
    """

    # connecting datbase and load it into pandas dataframe
    con = sqlite3.connect(db_path)
    tweet_df = pd.read_sql_query("SELECT * FROM tweetscapture ORDER BY Date DESC", con)

    #creating a column month and year for data seperation
    # -- creating the columns and adding the data
    tweet_df["year"] = tweet_df["Date"].apply(get_year)
    tweet_df["month"] = tweet_df["Date"].apply(get_month)

    # stdout of how much memory used when loading df
    memory_usage = tweet_df.memory_usage(deep=True).sum()/1024**2
    print(f"Total Memory used: {round(memory_usage, 2)} MB")

    return tweet_df


if __name__ == "__main__" :

    #CLI args
    desc = "Script that setups up tweet database into a file system"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-d", "--db", type=str, required=True,
                        help="path to database")
    args = parser.parse_args()

    # loading database
    tweet_df = load_as_dataframe(args.db)

    # creating data folder
    # TODO: This needs to be replaced with the designed paths in the Paths module
    paths = TweetAnalysisPaths()
    tweet_path = paths.tweet_data

    # grouping data based on month and year
    grouped_df = tweet_df.groupby(by=["year", "month"], axis=0)
    for year_month_id, year_df in grouped_df:

        #
        year = year_month_id[0]
        dir_data_path= os.path.join(tweet_path, year)

        # then group based on month
        # -- this will seperated all months
        grouped_month = year_df.groupby(by=["month"])
        for month, month_df in grouped_month:

            # creating complete path where to save csv file
            data_file_path = os.path.join(tweet_path, year, f"{int(month)}.tsv")


            # creating directories and csv files
            data_path = Path(dir_data_path)
            data_path.mkdir(parents=True, exist_ok=True)

            # saving as csv file
            month_df.to_csv(data_file_path, index=False, sep="\t")
            print("MESSAGE: Tweet data saved in:", data_file_path)