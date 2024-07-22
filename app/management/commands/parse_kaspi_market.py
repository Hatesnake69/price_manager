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
        chrome_options.add_argument("--headless")  # Если нужно запускать браузер в фоновом режиме
        chrome_options.add_argument("--disable-gpu")  # Отключение GPU для совместимости

        # Добавление заголовков
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0")
        chrome_options.add_argument(
            "accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8")
        chrome_options.add_argument("accept-language=en-US,en;q=0.5")
        chrome_options.add_argument("accept-encoding=gzip, deflate, br, zstd")
        chrome_options.add_argument("connection=keep-alive")
        chrome_options.add_argument(
            "cookie=ks.tg=9; k_stat=7f6bc9ec-d0cf-40d7-a919-6fc5e622c2ab; kaspi.storefront.cookie.city=750000000; current-action-name=Index")
        chrome_options.add_argument("upgrade-insecure-requests=1")
        chrome_options.add_argument("sec-fetch-dest=document")
        chrome_options.add_argument("sec-fetch-mode=navigate")
        chrome_options.add_argument("sec-fetch-site=none")
        chrome_options.add_argument("sec-fetch-user=?1")
        chrome_options.add_argument("priority=u=0, i")
        # chrome_options.binary_location = "/usr/bin/google-chrome"
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        driver.get("https://www.google.com")
        print(f"Google page title: {driver.title}")
        driver.get("https://kaspi.kz/shop/search/?text=105509884&q=%3AavailableInZones%3AMagnum_ZONE1&sort=relevance&filteredByCategory=false&sc=")
        # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "item-card__info")))
        title = driver.execute_script("return document.title;")

        print(f"KASPI page title: {title}")
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
