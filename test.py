from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

from telegram import ReplyKeyboardMarkup
from requests.auth import HTTPBasicAuth

import requests

KP_TOKEN = '66XDW7D-CT0MF9Z-GZB7XYF-65WAXFN'
KP_KEY = 'X-API-KEY'
URL_RANDOM = 'https://api.kinopoisk.dev/v1/movie/random'
HEADERS = {'Authorization': f'ApiKey {KP_KEY, KP_TOKEN}'}
auth = HTTPBasicAuth(KP_KEY, KP_TOKEN)
updater = Updater(token='5902172202:AAHewEIuOCNWpnyfWyVkiY1o7i8RlJrXFKU')


response = requests.get(URL_RANDOM, headers=HEADERS).json()
# random_movie = response[0].get('name')
print(response)
