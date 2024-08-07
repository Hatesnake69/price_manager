import re
import sys
import time
import traceback
from sys import stdout

import selenium
from django.core.management.base import OutputWrapper

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

from app.models import KaspiGoodsModel


class KaspiMarketParser:
    counter = 2
    stdout = OutputWrapper(stdout or sys.stdout)

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.binary_location = "/usr/bin/google-chrome"
        self.driver = webdriver.Chrome(
            options=chrome_options
        )

    def run(self):
        all_goods: list[KaspiGoodsModel] = KaspiGoodsModel.objects.all()
        for good in all_goods:
            if not good.kaspi_offer_url:
                self.get_good_offer_url(good=good)
            else:
                self.parse_good(good=good)

        self.stdout.write('Команда выполнена успешно!')

    def get_good_offer_url(self, good: KaspiGoodsModel):
        for i in range(self.counter):
            try:
                goods_sku = good.sku.split("_")[0]
                print(f"current on {good.model}, {goods_sku}")
                url = f"https://kaspi.kz/shop/search/?text={goods_sku}&q=%3AavailableInZones%3AMagnum_ZONE1&sort=relevance&filteredByCategory=false&sc="
                self.driver.get(url)
                print(f"Opened URL: {url}")
                print(f"Page title: {self.driver.title}")
                try:
                    first_product = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/shop/p/"]'))
                    )
                    # Получение ссылки
                    product_link = first_product.get_attribute('href')
                    good.kaspi_offer_url = product_link
                    good.save()
                    print(f"offer url was added for good {good.model}")
                    print(f"{good.kaspi_offer_url}")
                except selenium.common.exceptions.TimeoutException:
                    print("Element not found within the given time")
            except Exception as e:
                print(
                    f"An error occurred: \n{e}\n{traceback.format_exc()}"
                )
                time.sleep(1)

    def parse_good(self, good: KaspiGoodsModel):
        for i in range(self.counter):
            try:
                if good.no_competitors_flag:
                    return
                self.driver.get(good.kaspi_offer_url)
                try:
                    close_button = self.driver.find_element(By.CLASS_NAME, "icon.icon_close")
                    close_button.click()
                    print("close button!")
                except:
                    print("close button?")
                tbody = self.driver.find_element(By.TAG_NAME, "tbody")
                # iterate over all tr elements and print them
                tr_elements = tbody.find_elements(By.TAG_NAME, "tr")
                competitors = {}
                kaspi_price = good.price
                for tr in tr_elements:
                    td_elements = tr.find_elements(By.TAG_NAME, "td")
                    name = td_elements[0].find_element(By.TAG_NAME, "a").text
                    value = int(re.sub(r'\D', '', td_elements[3].text.strip()))
                    if name != "LED VISION KZ":
                        competitors[name] = value
                    else:
                        good.price = value
                        kaspi_price = value
                good.competitors_prices = competitors
                if not competitors:
                    good.prev_price = good.price
                    good.no_competitors_flag = True
                else:
                    min_price_name = min(competitors, key=competitors.get)
                    min_comp_price = competitors[min_price_name]
                    if kaspi_price >= min_comp_price:
                        new_price = round(min_comp_price * 0.99)
                        if new_price >= good.min_price:
                            good.prev_price = good.price
                            good.price = new_price
                        else:
                            good.min_price_too_high_flag = True
                            good.prev_price = good.price
                print(good)
                good.save()
                return
            except Exception as e:
                print(
                    f"An error occurred: \n{e}\n{traceback.format_exc()}"
                )
                time.sleep(1)
