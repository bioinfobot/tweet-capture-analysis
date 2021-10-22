import requests
import json
from collections import defaultdict
from bs4 import BeautifulSoup

def get_webpage() -> str:
    link = "https://en.wikipedia.org/wiki/List_of_programming_languages"
    r = requests.get(link)
    if r.status_code != 200:
        raise ConnectionError("Non 200 code was capture {}".format(r.status_code))

    content = r.text
    return content

def parse_webpage() -> dict: 
    """ Parses HTML and extracts all computer languages and their links.
    returns a dictioanry containing computer languages and links as key-value 
    pairs
    """
    content = get_webpage()
    bs = BeautifulSoup(content, features="html.parser")

    # source link
    wiki_link = "https://en.wikipedia.org"
    
    # selecting container that has all programing languages
    lang_elm_id = "mw-content-text"
    lang_table = bs.find(id=lang_elm_id)

    # selecing all the columns
    langs = defaultdict(lambda: None)
    divs = lang_table.find_all("div", {"class":"div-col"})
    for div in divs:
        list_elm = div.find_all("ul")
        for ul in list_elm:
            list_items = ul.find_all("li")
            for li in list_items:
                # error handlin when a link is not found 
                # -- string manipulation to remove unicode characters
                try:
                    endpoint = li.find("a").get("href")
                    link = "{}{}".format(wiki_link, endpoint)
                    lang = li.text.encode("ascii", "ignore").decode("utf-8")
                    langs[lang] = link 
                except AttributeError:
                    # some languages do not links so only append "N/A"
                    link = "N/A"
                    lang = li.text.encode("ascii", "ignore").decode("utf-8")
                    langs[lang] = link 
                
    return langs

if __name__ == "__main__":

    data = parse_webpage()
    with open("langs.json", "w") as outfile:
        json.dump(data, outfile)