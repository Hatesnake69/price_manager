import io
import openpyxl
from price_manager_project.settings import bot_token
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
import logging

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=bot_token)


if __name__ == "__main__":
    pass
