from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

from telegram import ReplyKeyboardMarkup

import requests

KP_TOKEN = '66XDW7D-CT0MF9Z-GZB7XYF-65WAXFN'
URL_RANDOM = 'https://api.kinopoisk.dev/v1/movie/random'
HEADERS = {'Authorization': f'OAuth {KP_TOKEN}'}
updater = Updater(token='5902172202:AAHewEIuOCNWpnyfWyVkiY1o7i8RlJrXFKU')
URL = 'https://api.thecatapi.com/v1/images/search'


def get_new_random():
    response = requests.get(URL).json()
    random_movie = response[0].get('name')
    return random_movie


def new_random(update, context):
    chat = update.effective_chat
    context.bot.send_message (chat.id, get_new_random())


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([
        ['/random', '/wisechoice'],
        ['/add', '/del']
    ], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо за доверие в выборе, {name}')
    context.bot.send_message(
        chat_id=chat.id,
        text='Для работы со мной используй меню, или команды: random - получить случайный фильм',
        reply_markup=button
    )


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('random', new_random))

updater.start_polling()
updater.idle()
