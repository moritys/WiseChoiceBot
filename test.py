from telegram import Update
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext
)

import requests
import os

from dotenv import load_dotenv


load_dotenv()

KP_TOKEN = os.getenv('KP_TOKEN')
KP_KEY = os.getenv('KP_KEY')
TG_TOKEN = os.getenv('TG_TOKEN')
URL_RANDOM = 'https://api.kinopoisk.dev/v1/movie/random'
HEADERS = {KP_KEY: KP_TOKEN}
updater = Updater(token=TG_TOKEN)
dispatcher = updater.dispatcher


def start_add(update, context) -> int:
    update.message.reply_text('Отправь мне ссылку на фильм (для отмены напиши /quit)')
    return ADD_MOVIE


def add_movie(update: Update, context: CallbackContext) -> int:
    url_movie = update.message.text.split('/')
    print(url_movie)
    movie_id = url_movie[-2]
    print(movie_id)
    # This variable needs to be stored globally to be retrieved in the next state
    update.message.reply_text(f'Айди фильма: {movie_id}')
    update.message.reply_text('Добавить фильм?')
    # Let the conversation proceed to the next state
    return CONFIRM


def confirm(update: Update, context: CallbackContext) -> int:
    answer = update.message.text
    if answer.lower() == 'нет':
        update.message.reply_text('Фильм не добавлен')
    elif answer.lower() == 'да':
        update.message.reply_text('Фильм добавлен!')
    else:
        update.message.reply_text('Общайся нормально')
    return ConversationHandler.END


def quit(update: Update, context: CallbackContext):
    return ConversationHandler.END


ADD_MOVIE, CONFIRM = 0, 1
dispatcher.add_handler(ConversationHandler(
    entry_points=[CommandHandler('add', start_add)],
    states={
        ADD_MOVIE: [MessageHandler(Filters.text, callback=add_movie)],
        CONFIRM: [MessageHandler(Filters.text, callback=confirm)]
    },
    fallbacks=[CommandHandler('quit', quit)]
))

updater.start_polling()
updater.idle()
