import time

from django.core.management import BaseCommand

from app.management.commands.utils.generate_xml import XmlGenerator
from app.management.commands.utils.parse_kaspi_market import KaspiMarketParser


class Command(BaseCommand):
    help = 'Запустить задачу по расписанию'
    parser: KaspiMarketParser

    def handle(self, *args, **kwargs):
        self.parser = KaspiMarketParser()
        self.doc_generator = XmlGenerator()
        self.stdout.write(self.style.SUCCESS('First run'))
        self.parser.run()
        self.doc_generator.run()
        time.sleep(30)
        self.stdout.write(self.style.SUCCESS('Scheduler started'))
        while True:
            self.parser.run()
            self.doc_generator.run()
            time.sleep(30)
