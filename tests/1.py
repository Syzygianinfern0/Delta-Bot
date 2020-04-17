# import time
# from utils.scrapers import get_results
from utils.toolkits import get_uploader_url

# url = get_uploader_url("Prof")
# for thing in get_results(url + "/1/"):
#     print(thing)
#     time.sleep(0.5)
import requests
from bs4 import BeautifulSoup as bs
import re

# response = requests.get("https://1337x.uproxy.workers.dev/torrent/3951854/Spider-Man-Homecoming-2017-1080p-x265-HEVC-10bit-BD-AAC-5-1-Prof/", headers={
response = requests.get('https://1337x.uproxy.workers.dev/sort-search/x265%20Prof/seeders/desc/1/', headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'})
soup = bs(response.text, "lxml")
resultset = soup.find('a', attrs={'href': re.compile("magnet.+")}).attrs['href']
print(resultset)
# print(response.text)
