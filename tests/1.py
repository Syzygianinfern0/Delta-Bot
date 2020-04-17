import time
from utils.scrapers import get_results
from utils.toolkits import get_uploader_url

url = get_uploader_url("Prof")
for thing in get_results(url + "/1/"):
    print(thing)
    time.sleep(0.5)
