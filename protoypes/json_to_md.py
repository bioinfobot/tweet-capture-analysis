# we are only testing with one script
import os  
import json

def to_markdown(json_data):
    pass

def send_to_contents(content_path):
    """Sends the .md files to conents
    
    Args:
    ----------
    content_path : str
        path to website content folder
    """
    pass


if __name__ == "__main__" :


    # parse json file
    json_file = "./2017-05.json"
    with open(json_file, "r") as infile:
        contents = infile.read()
    
    data = json.loads(contents)

    # selecting the important sections and formating it 
    top_languages = data["PopularLanguages"]
    hast_freq = data["HashFreq"]
    top_words = data["TopWords"]
    total_words = data["TotalWords"]
    img_url = data["ImageURL"]
    tweet_count = data["TweetCount"]
    user_freq = data["UsersFreq"]
    unique_words = data["UniqueWords"]

    # creating a writer class 


