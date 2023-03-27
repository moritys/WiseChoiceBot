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
URL_MOVIE_BY_ID = f'https://api.kinopoisk.dev/v1/movie/{id}'
HEADERS = {KP_KEY: KP_TOKEN}
updater = Updater(token=TG_TOKEN)
dispatcher = updater.dispatcher


def get_response_random():
    """Получение словаря данных о рандомном фильме."""
    response = requests.get(URL_RANDOM, headers=HEADERS).json()
    random_data_fields = {
        'random_movie_name': response.get('name'),
        'random_movie_rating': response.get('rating').get('kp'),
        'random_movie_year': response.get('year'),
        'random_movie_country': ', '.join([country['name'] for country in response.get('countries')]),
        'random_movie_genre': ', '.join([genre['name'] for genre in response.get('genres')]),
        'random_movie_description': response.get('description'),
        'random_movie_poster': response.get('poster').get('url'),
        'random_movie_url': response.get('id'),
        'random_movie_type': response.get('type'),
    }
    print('сделан запрос к кп')
    return random_data_fields


def get_data_random(update, context):
    """Отправка отформатированного сообщения /random."""
    chat = update.effective_chat
    random_data = {}

    for key, value in get_response_random().items():
        if value == None:
            random_data[key] = '-'
        random_data[key] = value

    if random_data['random_movie_type'] == 'tv-series':
        type_url = 'series'
    else:
        type_url = 'film'

    if random_data["random_movie_country"] == 'Россия':
        text_message = 'Здесь был Российский фильм, его я предлагать не буду.'
        image_message = 'static/notrussian.png'
        context.bot.send_photo(
            chat.id, photo=open(image_message, 'rb'), caption=text_message,
        )
    else:
        text_message = (
            f'*{random_data["random_movie_name"]}* \n'
            f'`Рейтинг: {random_data["random_movie_rating"]}` \n'
            f' \n'
            f'*Жанр:* {random_data["random_movie_genre"]} '
            f' \n'
            f'_({random_data["random_movie_country"]}, '
            f'{random_data["random_movie_year"]})_ \n'
            '---- \n'\
            f'{random_data["random_movie_description"]} \n'
            f'https://kinopoisk.ru/{type_url}/{random_data["random_movie_url"]}/'
        )
        image_message = random_data['random_movie_poster']
        context.bot.send_photo(
            chat.id, image_message,
            caption=text_message,
            parse_mode=ParseMode.MARKDOWN
        )


def new_random(update, context):
    """Обработка команды /random."""
    chat = update.effective_chat
    
    # первый рандомный фильм
    get_data_random(update, context)
    context.bot.send_message(chat.id, 'Либо посмотри вот это:')
    # второй рандомный фильм
    get_data_random(update, context)


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    text = (
        'Для работы со мной используй меню или команды: \n'
        '`/random` - получить два случайных фильма из КП \n'
        '`/wisechoice` - выбрать случайный фильм из своего списка \n'
        '`/add` - добавить фильм в коллекцию (ссылка должна быть с КП) \n'
        '`/del` - удалить фильм из коллекции (ссылка должна быть с КП) \n'
    )
    button = ReplyKeyboardMarkup([
        ['/random', '/wisechoice'],
        ['/add', '/del'],
    ], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо за доверие в выборе, {name}')
    context.bot.send_message(
        chat_id=chat.id,
        text=text,
        reply_markup=button,
        parse_mode=ParseMode.MARKDOWN
    )


def wisechoice(update, context):
    chat = update.effective_chat
    all_movie = get_all_user_movies_db(chat.id)
    movie_list = []
    for movie in all_movie:
        movie_list.append(movie[0])
    random_movie_id = random.choice(movie_list)

    text_message = f'Айди фильма: {random_movie_id}'
    context.bot.send_message(
        chat.id, text_message, parse_mode=ParseMode.MARKDOWN
    )


def start_add(update, context):
    update.message.reply_text('Отправь мне ссылку на фильм (для отмены напиши /quit)')
    return ADD_MOVIE


def add_movie(update, context):
    chat = update.effective_chat
    url_movie = update.message.text.split('/')
    movie_id = url_movie[-2]
    create_movie_table()
    add_movie_db(chat.id, movie_id)
    update.message.reply_text(f'Добавлен фильм с айди {movie_id}')
    return ConversationHandler.END


def del_movie(update, context):
    # проверить есть ли этот фильм в списке
    # удалить фильм из базы
    # добавить кнопку восстановления
    chat = update.effective_chat
    text_message = '_Функция пока в разработке_'
    context.bot.send_message(
        chat.id, text_message, parse_mode=ParseMode.MARKDOWN
    )


def about_random(update, context):
    chat = update.effective_chat
    text_message = (
        'Команда `/random` выбирает случайный фильмы с КП, если он: \n'
        '▸ вышел не более 10 лет назад \n'
        '▸ рейтинг больше `6` \n'
        '▸ жанр и страна любые'
    )
    context.bot.send_message(
        chat.id, text_message, parse_mode=ParseMode.MARKDOWN
    )

def quit_conv(update, context):
    return ConversationHandler.END

# random and base handlers
dispatcher.add_handler(CommandHandler('start', wake_up))
dispatcher.add_handler(CommandHandler('random', new_random))
dispatcher.add_handler(CommandHandler('wisechoice', wisechoice))
dispatcher.add_handler(CommandHandler('about_random', about_random))

# conversation handlers
# add movies
ADD_MOVIE = 0
dispatcher.add_handler(ConversationHandler(
    entry_points=[CommandHandler('add', start_add)],
    states={
        ADD_MOVIE: [MessageHandler(Filters.text, callback=add_movie)],
    },
    fallbacks=[CommandHandler('quit', quit_conv)]
))
# del movies
dispatcher.add_handler(CommandHandler('del', del_movie))


updater.start_polling()
updater.idle()
