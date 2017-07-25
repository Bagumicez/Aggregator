import requests
from datetime import date
from bs4 import BeautifulSoup
from time import sleep
from parse.models import Order


URLS = ['https://freelance.ru/projects/?cat=4&spec=446',
        'https://freelance.ru/projects/?cat=4&spec=312']
PAGE_HEAD = '&page='


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
    list_date = str.split(' ')
    try:
        date_list = list_date[1].split('.')
    except:
        date_list = list_date[0].split('.')    
    year = int('20' + date_list[-1])
    month = int(date_list[1])
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
    pagination = soup.find('ul', class_='pagination')
    if pagination is not None:
        last_page_link = pagination.find_all('li')[-2]
        num = last_page_link.find('a')['href'].split('=')[-1]
        return int(num)
    else:
        return 1


def parse(html):
    proj_page = []
    soup = BeautifulSoup(html, 'lxml')
    root = soup.find('div', class_='projects')
    for proj in root.find_all('div', class_='proj'):
        title = proj.find('a', class_='ptitle').span.text
        price = proj.find('span', class_='cost').a.text
        url = proj.find('a', class_='ptitle')
        descr_url = 'https://freelance.ru' + url['href']
        try:
            descr_page = BeautifulSoup(get_html(descr_url), 'lxml')
            descr = descr_page.find('p', class_='txt').text
        except AttributeError:
            descr = ''
        meta = proj.find('ul', class_='list-inline').find_all('li')
        date = meta[0].text
        responses = meta[1].a.i.text

        proj_page.append({
            'title': title,
            'price': price,
            'url': 'https://freelance.ru' + url['href'],
            'description': descr,
            'time': str(format_date(date)),
            'responses': responses,
        })
    return proj_page


def main():
    all = []
    for url in URLS:
        total_pages = get_total_page(url)
        if total_pages != 1:
            for page in range(1, total_pages + 1):
                cur_url = url + PAGE_HEAD + str(page)
                cur_html = get_html(cur_url)
                cur_res = parse(cur_html)
                if need_update(cur_res):
                    all.append(cur_res)
                else:
                    break
        else:
            cur_html = get_html(url)
            cur_res = parse(cur_html)
            if need_update(cur_res):
                all.append(cur_res)
    return all


if __name__ == '__main__':
    main()
