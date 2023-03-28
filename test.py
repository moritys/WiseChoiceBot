from telegram import Update, ReplyKeyboardMarkup, ParseMode
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

from db_connection import add_movie_db, create_movie_table, del_movie_db, get_all_user_movies_db
import random


load_dotenv()

KP_TOKEN = os.getenv('KP_TOKEN')
KP_KEY = os.getenv('KP_KEY')
TG_TOKEN = os.getenv('TG_TOKEN')
URL_RANDOM = 'https://api.kinopoisk.dev/v1/movie/random'
URL_MOVIE_BY_ID = 'https://api.kinopoisk.dev/v1/movie/'
HEADERS = {KP_KEY: KP_TOKEN}
updater = Updater(token=TG_TOKEN)
dispatcher = updater.dispatcher


def add_id(id):
    global URL_MOVIE_BY_ID
    some = ''.join(str(id))
    print(some)
    URL_MOVIE_BY_ID += some
    print(URL_MOVIE_BY_ID)
    response = requests.get(URL_MOVIE_BY_ID, headers=HEADERS).json()
    print(response)
    movie_name = response.get('name')

    print(f'Удален фильм "{movie_name}"')
add_id(666)