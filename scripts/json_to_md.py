# TODO: only get latest file
# TODO: update with path's object
# we are only testing with one script
import os
import sys
import argparse
import glob
import json
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

# user made modules
sys.path.append("..")
from src.biobotpaths.paths import BioBotEndPoints
from bioinfobot.utils.paths import WebsitePaths, TweetAnalysisPaths


def to_markdown(json_file: str) -> str:
    """Reads in JSON file and converts it into markdown file

    paramters
    ---------
    json_file : str
        path to json file data

    returns
    -------
    str
        absolute path to the generated md file
    """

    # parse json file
    print("Compiling {}".format(os.path.basename(json_file)))
    with open(json_file, "r") as infile:
        contents = infile.read()

    data = json.loads(contents)

    # selecting the important sections and formating it
    top_languages = data["PopularLanguages"]
    hash_freq = data["HashFreq"]
    top_words = data["TopWords"]
    total_words = data["TotalWords"]
    tweet_count = data["TweetCount"]
    user_freq = data["UsersFreq"]
    unique_words = data["UniqueWords"]

    tweet_paths = TweetAnalysisPaths()
    name = os.path.splitext(os.path.basename(json_file))[0]
    mdpath = "../data/{}.md".format(name)
    date = datetime.now().strftime("%Y-%m-%d")

    # creating a file and appending data into the file
    with open(mdpath, "w") as mdfile:
        # md file meta data settings
        mdfile.write("+++\n")
        mdfile.write('title = "{} data"\n'.format(name))
        mdfile.write('description = "Overall twitter data of month {}"\n'.format(name))
        mdfile.write("date = {}\n".format(date))
        mdfile.write("comment = true\n")
        mdfile.write("draft = false\n")
        mdfile.write("diagram = false\n")
        mdfile.write('categories = ["Markdown"]\n')
        mdfile.write("+++\n")
        mdfile.write("\n")

        # adding word cloud image
        month = datetime.now().strftime("%Y-%m")
        mdfile.write("## Summary\n")
        img_tag = os.path.splitext(os.path.basename(json_file))[0]
        img_path = f"{tweet_paths.images_path}/{img_tag}.png"
        mdfile.write('![Summary Image]({} "Summary Image")\n'.format(img_path))
        summary_msg = "Analytical results for {} based on {} tweets consisting of {} total words with {} unique words\n".format(
            month, tweet_count, total_words, unique_words
        )

        mdfile.write("{}\n".format(summary_msg))
        mdfile.write("\n")

        # top 20 words
        mdfile.write("## Top 20 words\n")
        top_words_string = ", ".join(
            ["{}({})".format(word_info[0], word_info[1]) for word_info in top_words]
        )
        mdfile.write("{}\n".format(top_words_string))
        mdfile.write("\n")

        # top 20 tweeters
        mdfile.write("## Top 20 tweeters\n")
        user_string = ", ".join(
            [
                "[@{0}](https://twitter.com/{0})({1})".format(
                    user_info[0], user_info[1]
                )
                for user_info in user_freq
            ]
        )
        mdfile.write("{}\n".format(user_string))
        mdfile.write("\n")

        # top 20 hastags
        mdfile.write("## top 20 hastags\n")
        hash_string = " ".join(
            [
                "[{}](https://twitter.com/hashtag/{})({})".format(
                    hash_info[0], hash_info[0].replace("#", ""), hash_info[1]
                )
                for hash_info in hash_freq
            ]
        )
        mdfile.write("{}\n".format(hash_string))
        mdfile.write("\n")

        # Popular languages and framework
        mdfile.write("## Popular languages\n")
        lang_string = " ".join(
            ["{}({})".format(lang_info[0], lang_info[1]) for lang_info in top_languages]
        )
        mdfile.write("{}\n".format(lang_string))

    full_md_path = os.path.abspath(mdpath)
    if not os.path.exists(full_md_path):
        raise FileNotFoundError("{} does not exist".format(full_md_path))

    return full_md_path


def send_to_website(files: str, dst: str, create_dir=False) -> None:
    """Sends files to the webstie code

    Args:
    ----------
    files : str
        Files being sent to the website-code.
    dst : str
        Path to directory were the files will be moved to/
    create_dir : bool (default: False)

    Returns
    -------
    None
        Moves file to destined path
    """
    dst_path = Path(dst)
    website_paths = WebsitePaths()

    # path check. Should only be restrictive to website-code path.
    if website_paths.root_name not in dst:
        raise ValueError("Provided destined does not point to website source code")
    elif dst_path.is_file():
        raise ValueError("dst parameter cannot be a file. It must be a directory")

    if create_dir is False:
        if not dst_path.exists():
            raise FileNotFoundError("Unable to find destined directory in source code")

        # check all files exist before moving
        for f_path in files:
            fpath = Path(f_path)
            if not fpath.exists():
                raise FileNotFoundError("Provides files do not exists")
            shutil.move(fpath, dst_path.abspath())

    # dst parameter will create a new directory
    if create_dir is True:

        # will raise an error if the directory already exists
        dst_path.mkdir(exist_ok=False)

        # moving all files
        for f_path in files:
            fpath = Path(f_path)
            if not fpath.exists():
                raise FileNotFoundError("Provides files do not exists")
            shutil.move(fpath, dst_path.absp)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Converts JSON files into md files")
    parser.add_argument("-i", "--input", nargs="+", required=True, help="JSON file")
    parser.add_argument(
        "-o",
        "--overwrite",
        default=False,
        action="store_true",
        required=False,
        help="converts all JSON files into md files and overwrite md files in the website",
    )
    args = parser.parse_args()

    # initialize paths and temp_file
    web_paths = WebsitePaths()
    tweet_paths = TweetAnalysisPaths()
    temp_dir = tempfile.mkdtemp()
    posts_path = web_paths.website_posts

    # if the overwrite options is true
    # -- convert all json file to md files and overwrite all md files in the website
    # NOTE: This might be removed in the future since we're only doing this oncejjjjjjjj
    if args.overwrite is True:
        json_files = glob.glob(f"{tweet_paths.data_path}/*.json")
        for json_file in json_files:
            md_path = to_markdown(json_file)
            shutil.move(md_path, temp_dir)

        # remove all old md files that exists in the website folder
        old_md_files = glob.glob(f"{posts_path}/*.md")
        print(old_md_files)
        if not os.path.exists(posts_path):
            raise FileNotFoundError("word cloud file not found")
        [os.remove(_old_md) for _old_md in old_md_files]

        # adding new md files
        md_files = glob.glob(f"{temp_dir}/*.md")
        for md_file in md_files:
            shutil.move(md_file, posts_path)

        # removing temporary files
        shutil.rmtree(temp_dir)

    # if adding a single file or multiple files without overwriting
    for json_file in args.input:
        md_path = to_markdown(json_file)
        shutil.move(md_path, temp_dir)

    # if the file exists already, it will over write it
    added_md = glob.glob(f"{temp_dir}/*.md")
    [shutil.move(md, posts_path) for md in added_md]

    # remove temporary directory
    shutil.rmtree(temp_dir)





    

