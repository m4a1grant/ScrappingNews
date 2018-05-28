import requests
import datetime
from bs4 import BeautifulSoup
import csv

BASE_URL = 'https://globalnews.ca/search/facebook/'
#https://globalnews.ca/search/facebook/?post_type=any&orderby=&paged=6&ajax=true

def get_html(url):
    return requests.get(url).text


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    gnca_search_wrap = soup.find('div', id='gnca-search-wrap')
    articles = gnca_search_wrap.find_all('article')
    result = []
    for art in articles:
        data = {}
        link = art.find('h3', class_='story-h').find('a')
        data['link'] = link.get('href')
        data['text'] = link.contents[0].strip()
        dt = soup.find('h6', class_='story-date').contents[0].strip()
        data['date'] = get_iso_date(dt)
        result.append(data)
    #print(result[0])
    add_to_csv(result)


def get_iso_date(date):
    iso_date = datetime.datetime.strptime(date, "Published %B %d, %Y").date()
    return str(iso_date)


def add_to_csv(data):
    with open('result.csv', 'w', newline='') as output:
        field_names = ['text', 'link', 'date']
        writer = csv.DictWriter(output, field_names)
        writer.writeheader()
        for i in data:
            writer.writerow(i)



def main():
    html = get_html(BASE_URL)
    get_data(html)


if __name__ == '__main__':
    main()
