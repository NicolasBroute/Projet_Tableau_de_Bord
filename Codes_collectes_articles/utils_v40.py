import csv
import datetime as date
import json
import os
import bs4
import requests
from hashlib import md5
import unidecode
import re


def add_to_index(date_publi, text, newspaper):
    hash_text = get_hash(date_publi, text, newspaper)
    with open("hash_text.csv", "a") as f:
        f.write(hash_text + ",")


def get_hash(date_publi, text, newspaper):
    """create a hash from the date, the title, and the newspaper to find
    if an article already exists
    Arguments:
        date {string} -- date of the article
        text {string} -- title of the article
        newspaper {string} -- name of the newspaper
    Returns:
        string -- a hash of the article
    """

    hash = md5("{} {} {}".format(date_publi, text, newspaper).encode())
    return hash.hexdigest()


def already_exists(date_publi, text, newspaper):
    """create a test to see if the article entered already exists
    Arguments:
        date {string} -- date of the article
        text {string} -- title of the article
        newspaper {string} -- name of the newspaper
    Returns:
        boolean -- False: Doesn't exist | True: Does exist
    """

    hash_text = get_hash(date_publi, text, newspaper)
    with open("hash_text.csv", "r") as f:
        csv_reader = csv.reader(f, delimiter=",")
        already_existing_hash = csv_reader.__next__()[:-1]
    return hash_text in already_existing_hash


def create_index():
    """Create the index for all the article saved
    """
    try:

        source = "/var/www/html/projet2018/data/clean/robot/"
        dates_extract = os.listdir(source)

        hash_text = []

        for date_extract in dates_extract:
            source_date = source + date_extract + "/"
            for newspaper in os.listdir(source_date):
                source_newpaper = source_date + newspaper + "/"

                for article in os.listdir(source_newpaper):
                    u8 = "utf-8"
                    with open(source_newpaper + article, "r", encoding=u8) \
                            as f:
                        data = json.load(f)
                        title = data["title"]
                        date_publi = data["date_publi"]
                        newspaper = data["newspaper"]

                    hash_text.append(get_hash(date_publi, title, newspaper))

        hash_text = list(set(hash_text))

        with open("hash_text.csv", "a") as f:
            f.write(",".join(hash_text)+",")
        print("creer")

    except:
        with open("hash_text.csv", "w") as f:
            f.write(",")
            print("creer")


def create_json(file_target, list_article, sources, abbreviation):
    """
    Entree:
        file_target: string containing the path of the folder
        sources: string containing folder name
        list_article: list containing new articles
        abbreviation:string containing the journal abbreviation
    Exit:
        one json file per item
    For each article, the function creates a json file named after it:
        art_abreviation_numeroArticle_datejour_robot. json.
    It places the json file in the folder corresponding to the journal
    if it exists otherwise it creates it.
    """
    os.makedirs(file_target+sources, exist_ok=True)
    list_file = os.listdir(file_target+sources)
    num_max = 0
    if list_file:
        list_num = []
        for file in list_file:
            delimiter = file.split("_")
            list_num.append(delimiter[2])
        for num in list_num:
            num_max = max(num_max, int(num))
    ii = num_max + 1

    cur_date = date.datetime.now().date()
    for article in list_article:
        if not already_exists(article["date_publi"], article["title"],
                              article["newspaper"]):
            add_to_index(article["date_publi"], article["title"],
                         article["newspaper"])
            if "/" in sources:
                file_art = file_target + sources + "art_" + abbreviation + "_"\
                    + str(ii) + "_" + str(cur_date) + "_robot.json"
            else:
                file_art = file_target + sources + "/" + "art_" + abbreviation\
                 + "_" + str(ii) + "_" + str(cur_date) + "_robot.json"
            with open(file_art, "w", encoding="UTF-8") as fic:
                json.dump(article, fic, ensure_ascii=False)

            ii += 1


def recovery_article(title, newspaper, authors, date_publi, content, theme):
    """
    Arguments:
        title : string
        newspaper : string
        authors : list
        date_publi : string
        content : string
        theme : string
    Return : dictionary containing title, newspaper,
    """
    for ii in range(len(authors)):
        authors[ii] = unidecode.unidecode(authors[ii])

    content = re.sub(r"\s\s+", " ", content)
    content = re.sub(r"\s", " ", content)

    new_article = {
                "id_art": get_hash(date_publi, title, newspaper),
                "title": unidecode.unidecode(title),
                "newspaper": unidecode.unidecode(newspaper),
                "author": authors,
                "date_publi": date_publi,
                "content": unidecode.unidecode(content),
                "theme": unidecode.unidecode(theme)
        }
    return(new_article)


def is_empty(article):
    """
    Argument :
        article : dictionary
    Add the article if the content, the publication date and the title
        are not empty
    """
    if (article["content"] != ""
            and article["title"] != ""
            and article["date_publi"] != ""):
        return False

    return True


def recovery_flux_url_rss(url_rss):
    """
    Arguments:
        string containing the url of the rss feed
    Return :
        object containing the parse page
    The function parse the page with beautifulsoup
    """
    req = requests.get(url_rss)
    data = req.text
    soup = bs4.BeautifulSoup(data, "lxml")
    return(soup)


if __name__ == '__main__':
    create_index()