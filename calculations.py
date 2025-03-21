import requests
import urllib.parse
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# разобьем на 15 районов
rayons = [
    "Пушкино",
    "Ногинск",
    "Подольск",
    "Балашиха",
    "Серпухов",
    "Долгопрудный",
    "Лобня",
    "Реутов",
    "Красногорск",
    "Старая_Купавна",
    "Видное",
    "Сергиев_Посад",
    "Мытищи",
    "Химки",
    "Люберцы"
]


dict_coords = {}
lat_list=[]
lon_list=[]
# спарсим координаты наших районов
base_url = "https://ru.wikipedia.org/wiki/"
pattern = r'"wgCoordinates":\{"lat":([\d.]+),"lon":([\d.]+)\}'

for rayon in rayons:
    encoded_country_name = urllib.parse.quote(rayon)
    url_country = base_url + encoded_country_name
    html_country = requests.get(url_country).text
    data = html_country
    match = re.search(pattern, data)
    lat = float(match.group(1))
    lon = float(match.group(2))
    dict_coords[rayon] = (lon, lat)
    lat_list.append(lat)
    lon_list.append(lon)


url_kreml = "https://ru.wikipedia.org/wiki/Московский_Кремль"
html_kreml = requests.get(url_kreml).text
data = html_kreml
match = re.search(pattern, data)
lat_k = float(match.group(1))
lon_k = float(match.group(2))
kreml_coords = (lon_k, lat_k)

# теперь найдем расстояние между районом (средней точкой, которую мы получили) и Московским Кремлем - среднее расположение нашей целевой аудитории

url_coords = 'https://calculatorium.net/geography/distance-between-two-coordinates'
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get(url_coords)


def calculate_distance(coords_1: tuple, coords_2: tuple):
    lon_1_input = driver.find_element(By.ID, 'twocoordinatesform-longitude1')
    lon_1_input.send_keys(coords_1[0])

    lat_1_input = driver.find_element(By.ID, "twocoordinatesform-latitude1")
    lat_1_input.send_keys(coords_1[1])

    lon_2_input = driver.find_element(By.ID, 'twocoordinatesform-longitude2')
    lon_2_input.send_keys(coords_2[0])

    lat_2_input = driver.find_element(By.ID, "twocoordinatesform-latitude2")
    lat_2_input.send_keys(coords_2[1])

    calculate_button = driver.find_element(By.CLASS_NAME, "btn-success")
    calculate_button.click()
    time.sleep(3)

    if "calculatorium.net" not in driver.current_url:  # ищем редиректы (перекидывает на казино)
        driver.back()
        time.sleep(3)

    element = driver.find_element(By.ID, 'result')
    distance = element.text.strip()
    distance = float(distance.replace(' км', ''))

    lon_1_input.clear()
    lat_1_input.clear()
    lon_2_input.clear()
    lat_2_input.clear()
    time.sleep(1)
    return distance

dict_distance = {}

for rayon in rayons:
    distance_to_kreml = calculate_distance(kreml_coords, dict_coords[rayon])
    dict_distance[rayon] = distance_to_kreml

dict_prices = {  # получили из файла Prices.py
    "Пушкино": 15600.0,
    "Ногинск": 15600.0,
    "Подольск": 12294.5,
    "Балашиха": 12600.0,
    "Серпухов": 16500.0,
    "Долгопрудный": 26415.5,
    "Лобня": 13500.0,
    "Реутов": 18000.0,
    "Красногорск": 15000.0,
    "Старая_Купавна": 10200.0,
    "Видное": 15800.0,
    "Сергиев_Посад": 9910.0,
    "Мытищи": 14635.0,
    "Химки": 13200.0,
    "Люберцы": 14572.0
}

df = pd.DataFrame({
    'Цена': pd.Series(dict_prices),
    'Расстояние': pd.Series(dict_distance),
    'Долгота': lon_list,
    'Широта': lat_list
})

# Устанавливаем названия районов в качестве индекса
df.index.name = 'Район'

print(df.head(15))