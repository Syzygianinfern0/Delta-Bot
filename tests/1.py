from utils.scrapers import get_results
from utils.toolkits import get_uploader_url
url = get_uploader_url('Prof')
for thing in get_results(url):
    print(thing)