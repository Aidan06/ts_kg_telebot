import requests
from bs4 import BeautifulSoup


def send(url):
    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.text


def get_days_series_from_site(news_days, url):
    response_data = send(url=url)
    soup = BeautifulSoup(response_data, 'lxml')
    soup = soup.find_all('a', class_='news-link app-news-link')

    for i, s in enumerate(soup, start=1):
        news_day = []
        if s.findChildren('a', class_='sub'):
            for j, sub_c in enumerate(s.findChildren('a', class_='sub'), start=1):
                news_days.append(
                    {'id': f'{i}.{j}', 'name': sub_c.text, 'url': sub_c.get('href')}
                )

        news_days.append(
            {
                'id': f'{i}',
                'name': s.findChildren('a', 'app-news-date')[0].text,
                'url': s.findChildren('a', 'app-news-date')[0].get('href'),
                'news_day': news_day,
            }
        )


def series_in_a_day(series: list, url):
    series.clear()
    response_data = send(url=url)
    soup = BeautifulSoup(response_data, 'lxml')
    soup = soup.find_all('a', class_='news-link app-news-link')

    for s in soup:
        series.append({'name': s.text})