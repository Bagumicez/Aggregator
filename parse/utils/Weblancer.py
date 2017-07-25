import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import date
from parse.models import Order


KEYWORDS = ['python', 'django', 'machine learning']
PAGE_PIECE = '&page='
KEYWORD_PIECE = '&keywords='
DOMEN = 'https://www.weblancer.net'
BASE_URL = 'https://www.weblancer.net/jobs/?action=search'


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


def prepare_network():
    global s
    s = requests.Session()
    s.get('https://www.weblancer.net/')


def format_date(str):
    dates = str.split('.')
    formated_time = date(int(dates[-1]), int(dates[1]), int(dates[0]))
    return formated_time


def get_html(url):
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/59.0.3071.115 Safari/537.36'}
    response = s.get(url, headers=headers)
    sleep(2)
    return response.content


def get_total_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    try:
        pagination = soup.find('ul', class_='pagination').find_all('li')
        num = pagination[-1].a.get('href').split('&')[-1].split('=')[-1]
        return int(num)
    except AttributeError:
        return 1


def parse(html):
    orders = []
    soup = BeautifulSoup(html, 'lxml')
    root = soup.find('div', class_='container-fluid cols_table show_visited')
    all_oder = root.find_all('div', class_='row')
    for order in all_oder:
        title_url = order.find('h2', class_='title')
        title = title_url.a.text.strip()
        url = 'https://www.weblancer.net' + title_url.a.get('href')
        applications = order.find('div', class_='col-sm-3 text-right text-nowrap hidden-xs')
        try:
            responses = int(applications.text.strip().split(' ')[0])
        except:
            responses = 0
        time_ago = order.find('span', class_='time_ago').get('title').split(' ')[0]
        price = order.find('div', class_='col-sm-1 amount title').text.strip()
        descr_page = BeautifulSoup(get_html(url), 'lxml')
        try:
            info_block = descr_page.find_all('div', class_='col-sm-12')
            for div in info_block[1].find_all('div'):
                div.decompose()
            description = info_block[1].text.strip()
        except:
            continue
        orders.append({
            'title': title,
            'description': description,
            'price': price,
            'time': format_date(time_ago).__str__(),
            'responses': responses,
            'url': url
        })
    return orders


def main():
    all = []
    prepare_network()
    for name in KEYWORDS:
        total_page = get_total_page(BASE_URL + KEYWORD_PIECE + name)
        if total_page == 1:
            cur_url = BASE_URL + KEYWORD_PIECE + name
            cur_html = get_html(cur_url)
            cur_res = parse(cur_html)
            if need_update(cur_res):
                all.append(cur_res)
        else:
            for page in range(1, total_page+1):
                cur_url = BASE_URL + KEYWORD_PIECE + name + PAGE_PIECE + str(page)
                cur_html = get_html(cur_url)
                cur_res = parse(cur_html)
                if need_update(cur_res):
                    all.append(cur_res)
                else:
                    break
    return all


if __name__ == '__main__':
    main()