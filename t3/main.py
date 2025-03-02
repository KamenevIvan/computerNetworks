from fastapi import FastAPI, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, Ad
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

SQLALCHEMY_DATABASE_URL = "postgresql://parser_user:password@localhost/avito_parser"

app = FastAPI()

minPriceXPath = '//*[@id="app"]/div/buyer-location/div/div/div/div[3]/div/div[2]/div[3]/div[1]/div/div[3]/div[2]/div[2]/form/div[2]/div[2]/div/div/div/label[1]/div/div/input'
maxPriceXPath = '//*[@id="app"]/div/buyer-location/div/div/div/div[3]/div/div[2]/div[3]/div[1]/div/div[3]/div[2]/div[2]/form/div[2]/div[2]/div/div/div/label[2]/div/div/input'
showButton = '//*[@id="app"]/div/buyer-location/div/div/div/div[3]/div/div[2]/div[3]/div[1]/div/div[3]/div[2]/div[4]/div/div/button/span/span'
nextPageButton = '//*[@id="app"]/div/buyer-location/div/div/div/div[3]/div/div[2]/div[3]/div[3]/div[4]/nav/ul/li[9]/a'


# Конфигурация Selenium
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)


# Функция парсера
def parse_avito(url: str):
    driver = get_driver()  # Используем нашу функцию из предыдущего кода
    try:
        driver.get(url)

        # Переносим основные этапы парсинга
        wait = WebDriverWait(driver, 10)

        # --- Обработка фильтров ---
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

        # --- Парсинг страниц ---
        ads_data = []
        for i in range(5):
            ads_block = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'items-items-')]")
                )
            )

            all_ads = ads_block.find_elements(
                By.XPATH, ".//div[contains(@class, 'iva-item-root-')]"
            )

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
                        {
                            "title": title,
                            "price": price,
                            "link": link,
                            "location": location,
                        }
                    )
                except Exception as e:
                    print(f"Ошибка при обработке объявления: {e}")
                    continue

            # Переход на следующую страницу
            try:
                next_page = wait.until(
                    EC.presence_of_element_located((By.XPATH, nextPageButton))
                )
                driver.execute_script("arguments[0].scrollIntoView();", next_page)
                next_page.click()
                time.sleep(2)  # Небольшая пауза для загрузки
            except:
                print("Достигнут конец страниц")
                break

        # --- Сохранение в БД вместо CSV ---
        db = SessionLocal()
        try:
            for ad in ads_data:
                db.add(Ad(**ad))
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Ошибка записи в БД: {e}")
        finally:
            db.close()

    except Exception as e:
        print(f"Критическая ошибка: {e}")
    finally:
        driver.quit()


# Endpoint для запуска парсера
@app.get("/parse")
async def start_parse(url: str, background_tasks: BackgroundTasks):
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    background_tasks.add_task(parse_avito, url)
    return {"message": "Парсинг запущен в фоновом режиме"}


# Endpoint для получения данных
@app.get("/ads")
def get_ads():
    db = SessionLocal()
    try:
        ads = db.query(Ad).all()
        return [
            {
                "title": ad.title,
                "price": ad.price,
                "link": ad.link,
                "location": ad.location,
            }
            for ad in ads
        ]
    finally:
        db.close()
