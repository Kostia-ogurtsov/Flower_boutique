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

def sort_items(driver, url):
    driver.get(url)
    time.sleep(2)
    input_field = driver.find_element(By.CSS_SELECTOR, 'input[data-marker="price-to/input"]')

    input_field.clear()
    for digit in "1000":
        input_field.send_keys(digit)
        time.sleep(0.2)

    current_value = input_field.get_attribute("value").replace(" ", "")
    expected_value = "1000"
    assert current_value == expected_value, f"Ожидалось значение {expected_value}, но получено {current_value}"

    checkbox = driver.find_element(By.CSS_SELECTOR, '[data-marker="filters/byTitle/byTitle"]')
    actions = ActionChains(driver)
    actions.move_to_element(checkbox).click().perform()

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

    for page in range(1, page_count + 1):
        
        if driver.session_id is None:
            print("Перезапуск сессии браузера")
            driver = webdriver.Chrome()
            driver.get(f"{url}&p={page}")
        else:
            driver.get(f"{url}&p={page}")
        driver.implicitly_wait(3)    
        price_elements = driver.find_elements(By.CSS_SELECTOR, 'meta[itemprop="price"]')
        prices = [price_elements[i].get_attribute("content") for i in range(ads_count)]
        print(f"Page: {page}, Цены: {prices}")

url = 'https://www.avito.ru/moskva?q=роза+охара'
driver = driver_init()
cur_url = sort_items(driver, url)
get_prices(driver, cur_url)
driver.quit()

url = 'https://www.avito.ru/moskva?q=роза+бомбастик'
driver = driver_init()
cur_url = sort_items(driver, url)
get_prices(driver, cur_url)

url = 'https://www.avito.ru/moskva?q=роза+джульетта'
driver = driver_init()
cur_url = sort_items(driver, url)
get_prices(driver, cur_url)