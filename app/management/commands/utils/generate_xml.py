import sys
from sys import stdout


from django.core.management.base import OutputWrapper

from app.models import KaspiGoodsModel
from price_manager_project.settings import company_id, store_1_id, store_2_id, kaspi_prices_file_path


class XmlGenerator:
    stdout = OutputWrapper(stdout or sys.stdout)

    def run(self):
        xml_str = f"""
<?xml version="1.0" encoding="utf-8"?>
<kaspi_catalog date="string"
xmlns="kaspiShopping"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="kaspiShopping http://kaspi.kz/kaspishopping.xsd">
<company>LedVision</company>
<merchantid>{company_id}</merchantid>
<offers>
"""
        for row_idx, good in enumerate(KaspiGoodsModel.objects.order_by('id'), start=2):
            xml_str += f"""
<offer sku="{good.sku}">
<model>{good.model}</model>
<brand>{good.brand}</brand>
<availabilities>
<availability available={"yes" if good.pp1 else "no"} storeId="{store_1_id}"/>
<availability available={"yes" if good.pp2 else "no"} storeId="{store_2_id}"/>
</availabilities>
<price>{good.price}</price>
</offer>
"""
        xml_str += """
</offers>
</kaspi_catalog>
"""
        with open(kaspi_prices_file_path, "w+", encoding="utf-8") as file:
            file.write(xml_str)

        self.stdout.write('Команда выполнена успешно!')
