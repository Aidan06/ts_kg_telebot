import requests
from bs4 import BeautifulSoup


def manual_search(url):
    response_data = requests.get(url=url)
    soup = BeautifulSoup(response_data, 'lxml')
    print(soup)