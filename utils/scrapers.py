import re

import requests
from bs4 import BeautifulSoup as bs

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"
header = {'User-Agent': USER_AGENT}


def get_results(url: str):
    """
    :param url: Pagination without trailing '/'
    :param stop: Stops at page number
    :return: A generator object.
    """
    response = requests.get(url, headers=header)
    soup = bs(response.text, "lxml")
    resultset = soup.find_all("tr")[1:]
    if len(resultset) == 0:
        return
    for item in resultset:
        data = [i for i in item.children]
        follow_url = "https://1337x.uproxy.workers.dev"
        follow_url += data[1].contents[1].get("href")
        magnet = get_magnet_from_page(follow_url)
        seeds = data[3].contents[0]
        leeches = data[5].contents[0]
        size = data[7].contents[0]
        age = data[9].contents[0]

        yield {
            "magnet": magnet,
            "follow_url": follow_url,
            "seeds": seeds,
            "leeches": leeches,
            "size": size,
            "age": age,
        }


def get_magnet_from_page(url):
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    soup = bs(response.text, "lxml")
    resultset = soup.find('a', attrs={'href': re.compile("magnet.+")}).attrs['href']
    return resultset
