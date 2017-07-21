import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import date
import csv


BASE_URL = 'https://freelansim.ru/?'
PYTHON_HEAD = '&q=python'
PAGE_HEAD = '&page='


def format_date(str):
    date_time_list = str.split(',')
    date_list = date_time_list[0].split(' ')
    dict_of_mounth = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
                      'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
                      'сентября': 9, 'октрября': 10, 'ноября': 11, 'декабря': 12}
    year = int(date_list[-1])
    month = dict_of_mounth[date_list[1]]
    day = int(date_list[0])
    formated_date = date(year, month, day)
    return formated_date


def get_html(url):
    response = requests.get(url)
    sleep(4)
    return response.content


def get_total_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pagination = soup.find('div', class_='pagination')
    links = pagination.find_all('a')
    last_page = links[-2].get('href')
    return int(last_page.split('=')[1][0])


def parse(html):
    lists = []
    soup = BeautifulSoup(html, 'lxml')
    root = soup.find('ul', class_='content-list content-list_tasks')
    for proj in root.find_all('li', class_='content-list__item'):
        header = proj.find('div', class_='task__title')
        title = header.text
        url = 'https://freelansim.ru' + header.a.get('href')
        try:
            price_block = proj.find('span', class_='count')
            price_info = price_block.span.text
            price = price_block.text + ' ' + price_info
        except AttributeError:
            price = ''
        descr_html = get_html(url)
        description_page = BeautifulSoup(descr_html, 'lxml')
        descr = description_page.find('div', class_='task__description').text
        meta = description_page.find('div', class_='task__meta').text.split('\n')
        lists.append({
            'title': title.strip(),
            'description': descr.strip(),
            'price': price,
            'time': str(format_date(meta[1])),
            'url': url,
            'responses': meta[3],
            'views': meta[7]
        })

    return lists


def main():
    all = []
    total_pages = get_total_page(BASE_URL + PYTHON_HEAD)
    if total_pages != 1:
        for page in range(1, total_pages+1):
            cur_url = BASE_URL + PYTHON_HEAD + PAGE_HEAD + str(page)
            cur_html = get_html(cur_url)
            cur_res = parse(cur_html)
            all.append(cur_res)
    else:
        cur_url = BASE_URL + PYTHON_HEAD
        cur_html = get_html(cur_url)
        cur_res = parse(html)
        all.append(cur_res)
    return all

        


if __name__ == '__main__':
    main()
