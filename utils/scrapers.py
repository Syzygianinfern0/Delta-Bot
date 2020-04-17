import re

import requests
import telegram
from bs4 import BeautifulSoup as bs

from configs import *


def get_results(url: str, bot: telegram.Bot):
    """
    :param url: Pagination without trailing '/'
    :param bot: Bot Object
    :return: A generator object.
    """
    response = requests.get(url, headers=header)
    if len(response.content) == 0:
        bot.send_message(debugx_chat_id, "Proxy Response is empty")
    soup = bs(response.text, "lxml")
    resultset = soup.find_all("tr")[1:]
    if len(resultset) == 0:
        return
    for item in resultset:
        data = [i for i in item.children]
        follow_url = "https://1337x.uproxy.workers.dev"
        follow_url += data[1].contents[1].get("href")
        magnet = get_magnet_from_page(follow_url, bot)
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


def get_magnet_from_page(url, bot):
    response = requests.get(url, headers=header)
    if len(response.content) == 0:
        bot.send_message(debugx_chat_id, "Magnet Response is empty")
    soup = bs(response.text, "lxml")
    resultset = soup.find('a', attrs={'href': re.compile("magnet.+")}).attrs['href']
    return resultset
