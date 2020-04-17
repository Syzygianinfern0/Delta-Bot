import requests
from bs4 import BeautifulSoup as bs


def get_results(url: str, stop=2):
    """
    :param url: Pagination without trailing '/'
    :param stop: Stops at page number
    :return: A generator object.
    """
    for page in range(stop):
        response = requests.get(url + f"/{page+1}")
        soup = bs(response.text, "lxml")
        resultset = soup.find_all("tr")[1:]
        if len(resultset) == 0:
            return
        for item in resultset:
            data = [i for i in item.children]
            url = "https://1337x.to"
            url += data[1].contents[1].get("href")
            seeds = data[3].contents[0]
            leeches = data[5].contents[0]
            size = data[7].contents[0]
            age = data[9].contents[0]
            yield {
                "url": url,
                "seeds": seeds,
                "leeches": leeches,
                "size": size,
                "age": age,
            }
