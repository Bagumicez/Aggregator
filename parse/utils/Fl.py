import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import date

BASE_URL = 'https://www.fl.ru/projects/'
PAGE_PIECE = '?page='
KIND_PIECE = '&kind=5'

header = {
    "Host": "www.fl.ru",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.fl.ru/projects/?page=2&kind=5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": 1,
}
payload = {
    "action": "postfilter",
    "kind": 5,
    "pf_category": "",
    "pf_subcategory": "",
    "comboe_columns[1]": 0,
    "comboe_columns[0]": 0,
    "comboe_column_id": 0,
    "comboe_db_id": 0,
    "comboe": "Все+специализации",
    "location_columns[1]": 0,
    "location_columns[0]": 0,
    "location_column_id": 0,
    "location_db_id": 0,
    "location": "Все+страны",
    "pf_cost_from": "",
    "currency_text_columns[1]": 0,
    "currency_text_columns[0]": 2,
    "currency_text_column_id": 0,
    "currency_text_db_id": 2,
    "pf_currency": 2,
    "currency_text": "Руб",
    "pf_keywords": "",
}

keyword_list = ['flask', 'machine learning', 'django', 'python']


def format_date(str):
    date_list = str.split('.')
    new_date = date(int(date_list[-1]), int(date_list[1]), int(date_list[0]))
    return new_date


def prepare_network():
    global s
    s = requests.Session()
    s.get('https://www.fl.ru/projects/')
    s.post('https://www.fl.ru/projects/', data=payload)


def get_html(url):
    response = s.get(url, params=header)
    sleep(3)
    return response.content


def parse(html):
    order_list = []
    soup = BeautifulSoup(html, 'lxml')
    check = soup.find('div', id='b_ext_filter')
    try:
        check.find('div', class_='b-button b-button_flat b-button_flat_grey', recursive=True)
    except:
        raise AttributeError
    root = soup.find('div', class_='b-page__lenta', recursive=True).div
    orders = root.find_all('div')
    for order in orders:
        try:
            title_url = order.find('h2')
            url = 'https://www.fl.ru' + title_url.a.get('href')
            title = title_url.a.text
            price = order.script.text.split('>')[1].split('<')[0].strip()
            descr_html = get_html(url)
            descr_page = BeautifulSoup(descr_html, 'lxml')
            descr_block = descr_page.find('div', class_='b-layout__txt b-layout__txt_padbot_20').text.strip()
            time_block = descr_page.find('div', class_='b-layout__txt b-layout__txt_padbot_30', recursive=True)
            time_place = \
            time_block.find('div', class_='b-layout__txt b-layout__txt_fontsize_11').text.strip().split(' ')[0]
            time = format_date(time_place)
            views = order.find('div', class_='b-post__foot b-post__foot_padtop_15')
            elem = views.script.text.split('</span>')
            try:
                responses = int(elem[-1].split(' ')[0])
            except:
                responses = 0
            order_list.append({
                'title': title,
                'price': price,
                'url': url,
                'description': descr_block,
                'time': str(time),
                'responses': responses
            })
        except AttributeError:
            continue
    print(order_list)
    return order_list


def main():
    notes = []
    for word in keyword_list:
        payload['pf_keywords'] = word
        prepare_network()
        for count in range(1, 10):
            try:
                cur_url = BASE_URL + PAGE_PIECE + str(count) + KIND_PIECE
                cur_html = get_html(cur_url)
                cur_res = parse(cur_html)
                notes.append(cur_res)
            except AttributeError:
                break
        print(notes)
        print('=====')
    return notes


if __name__ == '__main__':
    main()
