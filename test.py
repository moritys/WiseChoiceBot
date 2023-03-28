from telegram import Update, ReplyKeyboardMarkup, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
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


def bot(update: Update, context: CallbackContext) -> None:

    update.message.reply_text("Beginning of inline keyboard")

    keyboard = [
        [
            InlineKeyboardButton("Button 1", callback_data='1'),
            InlineKeyboardButton("Button 2", callback_data='2'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Replying to text", reply_markup=reply_markup)

def func1():
    print('press1')


def func2():
    print('press2')


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    # This will define which button the user tapped on (from what you assigned to "callback_data". As I assigned them "1" and "2"):
    choice = query.data
    
    # Now u can define what choice ("callback_data") do what like this:
    if choice == '1':
        func1()

    if choice == '2':
        func2()


updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, bot))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
updater.idle()