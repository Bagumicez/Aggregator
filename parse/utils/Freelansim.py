import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import date
from parse.models import Order


BASE_URL = 'https://freelansim.ru/?'
KEYWORD_HEAD = '&q='
PAGE_HEAD = '&page='


KEYWORD_LIST = ['python', 'machine+learning']


def need_update(result):
    qnt = 0
    cur_len = len(result)
    for i in range(0, cur_len):
        if Order.objects.filter(url=result[i]['url']).exists():
            qnt += 1
    if qnt == cur_len:
        print('no need for update')
        return False
    else:
        return True


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
    sleep(2)
    return response.content


def get_total_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pagination = soup.find('div', class_='pagination')
    try:
        links = pagination.find_all('a')
        last_page = links[-2].get('href')
    except AttributeError:
        return 1
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
    for word in KEYWORD_LIST:
        total_pages = get_total_page(BASE_URL + KEYWORD_HEAD + word)
        if total_pages != 1:
            for page in range(1, total_pages+1):
                cur_url = BASE_URL + KEYWORD_HEAD + word + PAGE_HEAD + str(page)
                cur_html = get_html(cur_url)
                cur_res = parse(cur_html)
                if need_update(cur_res):
                    all.append(cur_res)
                else:
                    break
        else:
            cur_url = BASE_URL + KEYWORD_HEAD + word
            cur_html = get_html(cur_url)
            cur_res = parse(cur_html)
            if need_update(cur_res):
                all.append(cur_res)
    return all


if __name__ == '__main__':
    main()
