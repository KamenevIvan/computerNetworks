import time
import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


with open("avito_ads.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "price", "link", "location"])
    writer.writeheader()

driver = webdriver.Chrome()

driver.get(
    "https://www.avito.ru/novosibirsk?q=%D0%BD%D0%BE%D1%83%D1%82%D0%B1%D1%83%D0%BA%D0%B8+%D0%BD%D0%BE%D0%B2%D1%8B%D0%B5"
)

wait = WebDriverWait(driver, 10)

minPriceXPath = '//*[@id="app"]/div/buyer-location/div/div/div/div[3]/div/div[2]/div[3]/div[1]/div/div[3]/div[2]/div[2]/form/div[2]/div[2]/div/div/div/label[1]/div/div/input'
maxPriceXPath = '//*[@id="app"]/div/buyer-location/div/div/div/div[3]/div/div[2]/div[3]/div[1]/div/div[3]/div[2]/div[2]/form/div[2]/div[2]/div/div/div/label[2]/div/div/input'
showButton = '//*[@id="app"]/div/buyer-location/div/div/div/div[3]/div/div[2]/div[3]/div[1]/div/div[3]/div[2]/div[4]/div/div/button/span/span'

sortButton = '//*[@id="app"]/div/buyer-location/div/div/div/div[3]/div/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/span'
cheaperButton = "/html/body/div[6]/div[4]/div/div/div/button[2]/div"

nextPageButton = '//*[@id="app"]/div/buyer-location/div/div/div/div[3]/div/div[2]/div[3]/div[3]/div[4]/nav/ul/li[9]/a'


minPrice = wait.until(EC.presence_of_element_located((By.XPATH, minPriceXPath)))
driver.execute_script("arguments[0].scrollIntoView();", minPrice)
for char in "30000":
    minPrice.send_keys(char)
    time.sleep(0.2)

maxPrice = wait.until(EC.presence_of_element_located((By.XPATH, maxPriceXPath)))
for char in "70000":
    maxPrice.send_keys(char)
    time.sleep(0.2)

driver.find_element(By.XPATH, showButton).click()
"""
sortElem = wait.until(EC.presence_of_element_located((By.XPATH, sortButton)))
sortElem.click()

time.sleep(2) # Я не уверен, почему, но без задержки он отказвается видеть следующий элемент
cheaperElem = wait.until(EC.presence_of_element_located((By.XPATH, cheaperButton)))
cheaperElem.click()
"""
for i in range(5):
    wait = WebDriverWait(driver, 10)

    ads_block = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'items-items-')]")
        )
    )

    all_ads = ads_block.find_elements(
        By.XPATH, ".//div[contains(@class, 'iva-item-root-')]"
    )

    print(f"Найдено объявлений: {len(all_ads)}")

    ads_data = []
    for ad in all_ads:
        try:

            title = ad.find_element(
                By.XPATH, ".//div[contains(@class, 'iva-item-title-')]"
            ).text

            link = ad.find_element(
                By.XPATH, ".//a[contains(@class, 'iva-item-sliderLink-')]"
            ).get_attribute("href")

            price = ad.find_element(
                By.XPATH, ".//span[contains(@class, 'price-root-')]"
            ).text

            location = ad.find_element(
                By.XPATH, ".//div[contains(@class, 'geo-root-')]"
            ).text

            ads_data.append(
                {"title": title, "price": price, "link": link, "location": location}
            )
        except Exception as e:
            print(f"Ошибка при обработке объявления: {e}")

    with open("avito_ads.csv", "a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "price", "link", "location"])
        writer.writerows(ads_data)

    nexPage = wait.until(EC.presence_of_element_located((By.XPATH, nextPageButton)))
    driver.execute_script("arguments[0].scrollIntoView();", nexPage)
    driver.find_element(By.XPATH, nextPageButton).click()

    # time.sleep(2)

driver.quit()
