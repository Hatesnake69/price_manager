from django.core.management.base import BaseCommand

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


from app.models import KaspiGoodsModel


class Command(BaseCommand):
    help = 'Спарсить цены с каспи на товары'

    def handle(self, *args, **kwargs):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


        all_goods: list[KaspiGoodsModel] = KaspiGoodsModel.objects.all()
        for good in all_goods:
            if "_Ledvisionkz" in good.sku:
                goods_sku = good.sku.split("_")[0]
                url = f"https://kaspi.kz/shop/search/?text={goods_sku}&q=%3AavailableInZones%3AMagnum_ZONE1&sort=relevance&filteredByCategory=false&sc="
                driver.get(url)
                wait = WebDriverWait(driver, 0.1)
                first_product = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/shop/p/"]')))
                # Получение ссылки
                product_link = first_product.get_attribute('href')
                good.kaspi_offer_url = product_link
                good.save()
                print(f"offer url was added for good {good.model}")
                print(f"{good.kaspi_offer_url}")
        self.stdout.write(self.style.SUCCESS('Команда выполнена успешно!'))
