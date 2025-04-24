import time
import requests
from bs4 import BeautifulSoup
import numpy as np
import re

dict_rayons = {}

# чтобы корректно обращаться к ссылкам циана нужно ручками собрать эту информацию
rayons = {'pushkino': 175744,
          'noginsk': 317408,
          'podolsk': 4935,
          'balashikha': 174292,
          "serpukhov": 0,
          "dolgoprudny": 4738,
          "lobnya": 4848,
          "reutov": 4958,
          "krasnogorsk": 175071,
          "staraya-kupavna": 317389,
          "vidnoye": 174508,
          "sergiyev-posad": 175874,
          "mytishchi": 175378,
          "khimki": 5044,
          "lyubertsy": 175231}

for rayon in rayons.keys():
    prices = []

    url_first_page = f'https://{rayon}.cian.ru/snyat-sklad/'
    response = requests.get(url_first_page)
    html = response.text
    print(response.status_code)

    soup = BeautifulSoup(html, 'html.parser')
    factoid_items = soup.find_all('li', class_='_32bbee5fda--factoid-item--ABc2c')

    price_pattern = re.compile(r'(\d{1,3}(?:\s?\d{3})*)')

    for item in factoid_items:
        try:
            if item.find_previous('h3', class_='_32bbee5fda--title--zZuYF'):  # находим заголовок с Дополнительными предложениями, после него данные нерелевантны так как выдаются склады с рандомными адресами
                break
        except:
            pass
        text = item.get_text()
        if 'год' in text:
            match = price_pattern.search(text)
            if match:
                price = int(match.group(1).replace(' ', ''))
                prices.append(price)

    try:  # можем глянуть вторую страницу (дальше ссылки становятся немного неуправляемыми)
        url_next_page = f'https://{rayon}.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=offices&office_type%5B0%5D=3&p=2&region={rayons[rayon]}'
        html_new_page = requests.get(url_next_page).text

        title = soup.find('title').get_text()
        if 'Ошибка' in title:
            raise Exception

        soup = BeautifulSoup(html_new_page, 'html.parser')
        factoid_items = soup.find_all('li', class_='_32bbee5fda--factoid-item--ABc2c')

        for item in factoid_items:
            if item.find_previous('h3', class_='_32bbee5fda--title--zZuYF'):  # находим заголовок с Дополнительными предложениями, после него данные нерелевантны так как выдаются склады с рандомными адресами
                raise Exception
            text = item.get_text()
            if 'год' in text:
                match = price_pattern.search(text)
                if match:
                    price = int(match.group(1).replace(' ', ''))
                    prices.append(price)
    except Exception:
        pass

    print(f'Цены в {rayon}: {prices}')
    dict_rayons[rayon] = np.median(np.array(prices))
    print(dict_rayons[rayon], end='\n')
    time.sleep(60)  # не дает нормально парсить из-за ограничений на количество запросов по времени

print('\n')
print(dict_rayons)