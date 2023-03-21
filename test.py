from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

from telegram import ReplyKeyboardMarkup, ParseMode

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


response = requests.get(URL_RANDOM, headers=HEADERS).json()

listdict = response.get('genres')
genres = ', '.join([d['name'] for d in listdict if 'name' in d])
print(genres)



