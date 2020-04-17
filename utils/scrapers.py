import requests
from bs4 import BeautifulSoup as bs

MAGNET_LINK_CLASS = "l14efb2f6559484e5de81032020f86f3807c37a91 l87aa9eaddb6c504a87d8bc6c3f4786ce506dc2e3 l8e43fc27f870f333ea0aa3118280bf6d3e1785c4"


def get_results(url: str):
    """
    :param url: Pagination without trailing '/'
    :param stop: Stops at page number
    :return: A generator object.
    """
    response = requests.get(url)
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
    response = requests.get(url)
    soup = bs(response.text, "lxml")
    resultset = soup.find("a", {"class": MAGNET_LINK_CLASS})
    return resultset.attrs['href']
