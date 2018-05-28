import requests
import datetime
from bs4 import BeautifulSoup
import csv

BASE_URL = 'https://globalnews.ca/search/facebook/'

#https://globalnews.ca/search/facebook/?post_type=any&orderby=&paged=6&ajax=true

def get_html(url):
    result = ''
    for i in range(1, 11):
        payload = {'post_type': 'any',
                   'orderby': '',
                   'paged': i,
                   'ajax': 'true'}
        result += requests.post(url, data=payload).text
    return result


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find_all('article')
    result = []
    for art in articles:
        data = {}
        try:
            data['link'] = art.find('h3', class_='story-h').find('a').get('href')
        except:
            data['link'] = 'Can not find the link'
        try:
            data['text'] = art.find('h3', class_='story-h').find('a').text.strip()
        except:
            data['text'] = 'Can not find the link'
        try:
            dt = art.find('h6', class_='story-date').text.strip()
            data['date'] = get_iso_date(dt)
        except:
            data['date'] = 'Can not find the date'

        result.append(data)
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
