from telegram import Bot

from price_manager_project.settings import bot_token, admin_chat_id


def send_docs(docs: list):
    bot = Bot(token=bot_token)
    for doc in docs:
        bot.send_document(chat_id=admin_chat_id, document=doc)



