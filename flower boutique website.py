import requests
from bs4 import BeautifulSoup
import re

prices = []

def unique_flowers(url):
    global prices
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    price = soup.find('meta', {'itemprop': 'price'})

    if price:
        prices.append(price['content'])

names = ['Роза Охара', 'Роза Джульетта', 'Ранункулюс', 'Эвкалипт стабилизированный', 'Тюльпан красный', 'Тюльпан пионовидный розовый', 'Пион Гардения', 'Ирис синий']

urls = ['https://megacvet24.ru/rozy/roza-pink-ohara-50.html',
        'https://megacvet24.ru/rozy/roza-dzhuletta-50.html',
        'https://megacvet24.ru/cvety-optom/ranunkulyus-hanoy-optom.html',
        'https://megacvet24.ru/cvety-optom/evkalipt-cineriya-stabilizirovannyy-opt.html',
        'https://megacvet24.ru/cvety-optom/tyulpan-krasnyy-optom.html',
        'https://megacvet24.ru/tsvety/tyulpany/tyulpan-pionovidnyy-rozovyy.html',
        'https://megacvet24.ru/cvety-optom/pion-gardeniya-optom.html',
        'https://megacvet24.ru/cvety-optom/iris-siniy-optom.html']

for url in urls:
    unique_flowers(url)

print(prices)
