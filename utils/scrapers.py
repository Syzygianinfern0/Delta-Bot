import requests
from bs4 import BeautifulSoup as bs


def get_new_results(uploader: str):
    """
    ex: if url is 'https://1337x.to/user/goki/' then uploader field is 'goki'
    use the generator with next() untill  the func is_already_exist() returns True
    :param uploader: uploader name in the 1337x.to
    :return: A generator object.
    """
    # url = f'https://1337x.to/user/{uploader}/'
    for page in range(99):
        url = f'https://1337x.uproxy.workers.dev/{uploader}-torrents/{page}/'
        response = requests.get(url)
        soup = bs(response.text, 'lxml')
        resultset = soup.find_all('tr')[1:]
        if len(resultset) == 0:
            return
        for item in resultset:
            data = [i for i in item.children]
            url = 'https://1337x.to'
            url += data[1].contents[1].get('href')
            seeds = data[3].contents[0]
            leeches = data[5].contents[0]
            size = data[7].contents[0]
            age = data[9].contents[0]
            yield {'url': url,
                   'seeds': seeds,
                   'leeches': leeches,
                   'size': size,
                   'age': age
                   }
