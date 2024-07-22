import time

import selenium
from django.core.management.base import BaseCommand

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

from app.models import KaspiGoodsModel


class Command(BaseCommand):
    help = 'Спарсить цены с каспи на товары'

    def handle(self, *args, **kwargs):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.binary_location = "/usr/bin/google-chrome"
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        driver.get("https://www.google.com")
        print(f"Google page title: {driver.title}")
        driver.get("https://kaspi.kz/shop/search/?text=105509884&q=%3AavailableInZones%3AMagnum_ZONE1&sort=relevance&filteredByCategory=false&sc=")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "item-card__info")))
        print(f"KASPI page title: {driver.title}")
        all_goods: list[KaspiGoodsModel] = KaspiGoodsModel.objects.all()
        for good in all_goods:
            if "_Ledvisionkz" in good.sku:
                goods_sku = good.sku.split("_")[0]
                print(f"current on {good.model}, {goods_sku}")
                url = f"https://kaspi.kz/shop/search/?text={goods_sku}&q=%3AavailableInZones%3AMagnum_ZONE1&sort=relevance&filteredByCategory=false&sc="
                driver.get(url)
                print(f"Opened URL: {url}")
                print(f"Page title: {driver.title}")
                try:
                    first_product = WebDriverWait(driver, 20).until(
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

        self.stdout.write(self.style.SUCCESS('Команда выполнена успешно!'))
