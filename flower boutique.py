from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def driver_init():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def sort_items(driver, url, price_top):
    driver.get(url)
    time.sleep(2)
    input_field = driver.find_element(By.CSS_SELECTOR, 'input[data-marker="price-to/input"]')

    input_field.clear()
    for digit in price_top:
        input_field.send_keys(digit)
        time.sleep(0.2)

    current_value = input_field.get_attribute("value").replace(" ", "")
    assert current_value == price_top, f"Ожидалось значение {price_top}, но получено {current_value}"

    checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-marker="filters/byTitle/byTitle"]'))
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
    time.sleep(1)

    actions = ActionChains(driver)
    actions.move_to_element(checkbox).click().perform()
    time.sleep(1)

    aria_checked = checkbox.get_attribute("aria-checked")
    assert aria_checked == "true", f"Ожидалось значение 'true', но получено {aria_checked}"

    button = driver.find_element(By.CSS_SELECTOR, 'button[data-marker="search-filters/submit-button"]')
    button.click()
    time.sleep(2)
    current_url = driver.current_url

    return current_url

def get_prices(driver, url):
    driver.get(url)
    ads_count_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@data-marker='page-title/count']"))
    )
    ads_count_text = ads_count_element.text
    ads_count = int(ads_count_text.replace(' ', ''))

    if ads_count % 50 > 0:
        page_count = (ads_count // 50) + 1
    else:
        page_count = ads_count // 50

    d = {}
    for page in range(1, page_count + 1):
        driver.get(f"{url}&p={page}")
        driver.implicitly_wait(3)    

        items = driver.find_elements(By.CSS_SELECTOR, 'div[data-marker="item"]')
        for item in items:
            price = item.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute("content")
            link = item.find_element(By.CSS_SELECTOR, "a[itemprop='url']").get_attribute("href")
            d[int(price)] = link
    return d

def get_supplier(d, q, price_bottom):
    d = {key: value for key, value in d.items() if key > price_bottom}
    sorted_d = dict(sorted(d.items()))
    sorted_l = list(sorted_d.items())  
    if q < len(sorted_l):
        key, value = sorted_l[q]
        print(f"Поставщик, который предлагает минимальную цену {key}, доступен по ссылке {value}")


url = ['https://www.avito.ru/moskva?q=роза+охара',
       'https://www.avito.ru/moskva?q=роза+джульетта',
       'https://www.avito.ru/moskva?q=ранункулюс+цветы',
       'https://www.avito.ru/moskva?q=эвкалипт+стабилизированный',
       'https://www.avito.ru/moskva?q=тюльпан+красный+оптом',
       'https://www.avito.ru/moskva?q=тюльпан+пионовидный+оптом',
       'https://www.avito.ru/moskva?q=пион+цветы+оптом',
       'https://www.avito.ru/moskva?q=ирисы+цветы']

driver = driver_init()

#надо взять average prices с другого сайта и испоьзовать для каждого цветка свою
for i in range(len(url)):
    cur_url = sort_items(driver, url[i], "150")
    d = get_prices(driver, cur_url)
    for j in range(5):
        get_supplier(d, j, 40)

driver.quit()