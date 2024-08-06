import datetime

import telebot

from price_manager_project.settings import bot_token, admin_chat_id, tz


def send_docs(docs: list):
    bot = telebot.TeleBot(bot_token)
    for doc in docs:
        timestamp = datetime.datetime.now(tz).replace(microsecond=0, second=0)
        doc.name = f'KaspiGoods{timestamp.strftime("%Y%m%d%H%M")}.xlsx'
        bot.send_document(chat_id=admin_chat_id, document=doc)
