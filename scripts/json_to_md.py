# we are only testing with one script
import os  
import sys
import argparse
import glob
import json
import shutil
from datetime import datetime

# user made modules 
sys.path.append("..")
from src.biobotpaths.paths import BioBotEndPoints

def to_markdown(json_file):
    """ Reads in JSON file and converts it into markdown file"""

    
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
    img_url = data["ImageURL"]
    tweet_count = data["TweetCount"]
    user_freq = data["UsersFreq"]
    unique_words = data["UniqueWords"]


    name = os.path.splitext(os.path.basename(json_file))[0]
    fpath = "_temp_md_dir/{}.md".format(name)
    date = datetime.now().strftime("%Y-%m-%d")

    # creating a file and appending data into the file 
    with open(fpath, "w") as mdfile:
        mdfile.write("+++\n")
        mdfile.write('title = "{} data"\n'.format(name))
        mdfile.write('description = "Overall twitter data of month {}"\n'.format(name))
        mdfile.write('date = {}\n'.format(date))
        mdfile.write('comment = true\n')
        mdfile.write('draft = false\n')
        mdfile.write('diagram = false\n')
        mdfile.write('categories = ["Markdown"]\n') 
        mdfile.write("+++\n")
        mdfile.write("\n")

        # add image in json file 
        # NOTE: look at MD tutorial on how to add image 

        # add Summary data to
        # -- total_words in data
        # -- total_tweets in data 
        # -- total_unique_words in data 
        month = datetime.now().strftime("%Y-%m")
        mdfile.write("## Summary\n")
        summary_msg = "Analyical results for {} based on {} tweets consisting of {} total words with {} unique words\n".format(month, 
                                                                                                                        tweet_count, 
                                                                                                                        total_words,
                                                                                                                        unique_words)

        mdfile.write("{}\n".format(summary_msg))
        mdfile.write("\n")

        # top 20 words
        mdfile.write("## Top 20 words\n")
        top_words_string = ", ".join(["{}({})".format(word_info[0], word_info[1]) for word_info in top_words])
        mdfile.write("{}\n".format(top_words_string))
        mdfile.write("\n")

        # top 20 tweeters 
        mdfile.write("## Top 20 tweeters\n")
        user_string = ", ".join(["[@{0}](https://twitter.com/{0})({1})".format(user_info[0], user_info[1]) for user_info in user_freq])
        mdfile.write("{}\n".format(user_string))
        mdfile.write("\n")

        # top 20 hastags 
        mdfile.write("## top 20 hastags\n")
        hash_string = " ".join(["[{}](https://twitter.com/hashtag/{})({})".format(hash_info[0], hash_info[0].replace("#", ""), hash_info[1]) for hash_info in hash_freq])
        mdfile.write("{}\n".format(hash_string))
        mdfile.write("\n")
    
        # Popular lagnauges and framework
        mdfile.write("## Popular lagnauges\n")
        lang_string = " ".join(["{}({})".format(lang_info[0], lang_info[1]) for lang_info in top_languages])
        mdfile.write("{}\n".format(lang_string))

    


def send_to_contents(md_dir):
    """Sends the .md files to conents
    
    Args:
    ----------
    md_dir : str
        md directory that contains all the md files
    """
    # assuming this is in the scripts folder
    endpoint = BioBotEndPoints()
    content_path = "../../{}".format(endpoint.contents)
    print("Message sending mdfiles to website-code contents folder") 
    md_files = glob.glob("{}/*.md".format(md_dir))
    for md_file in md_files:
       shutil.move(md_file, content_path) 
        
    os.rmdir(md_dir) 


if __name__ == "__main__" :


    json_files = glob.glob("../data/*.json")
    temp_dir = "_temp_md_dir"
    if os.path.exists(temp_dir):
        os.remove(temp_dir)
    os.mkdir(temp_dir)
    for json_file in json_files:
        to_markdown(json_file)

    send_to_contents(temp_dir) 

