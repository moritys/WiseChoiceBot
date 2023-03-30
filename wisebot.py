from telegram import (
    Update, InlineKeyboardButton, ReplyKeyboardMarkup, ParseMode,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
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


def get_response(url):
    """Получение словаря данных о фильме."""
    response = requests.get(url, headers=HEADERS).json()
    data_fields = {
        'movie_name': response.get('name'),
        'movie_rating': response.get('rating').get('kp'),
        'movie_year': response.get('year'),
        'movie_country': ', '.join([country['name'] for country in response.get('countries')]),
        'movie_genre': ', '.join([genre['name'] for genre in response.get('genres')]),
        'movie_description': response.get('description'),
        'movie_poster': response.get('poster').get('url'),
        'movie_url': response.get('id'),
        'movie_type': response.get('type'),
    }

    return data_fields


def get_data_random(update, context):
    """Отправка отформатированного сообщения /random."""
    chat = update.effective_chat
    random_data = {}

    for key, value in get_response(URL_RANDOM).items():
        if value == None:
            random_data[key] = '-'
        random_data[key] = value

    if random_data['movie_type'] == 'tv-series':
        type_url = 'series'
    else:
        type_url = 'film'

    if random_data['movie_country'] == 'Россия':
        text_message = 'Здесь был Российский фильм, его я предлагать не буду.'
        image_message = 'static/notrussian.png'
        context.bot.send_photo(
            chat.id, photo=open(image_message, 'rb'), caption=text_message,
        )
    else:
        text_message = (
            f'*{random_data["movie_name"]}* \n'
            f'`Рейтинг: {random_data["movie_rating"]}` \n'
            f' \n'
            f'*Жанр:* {random_data["movie_genre"]} '
            f' \n'
            f'_({random_data["movie_country"]}, '
            f'{random_data["movie_year"]})_ \n'
            '---- \n'\
            f'{random_data["movie_description"]} \n'
            f'https://kinopoisk.ru/{type_url}/{random_data["movie_url"]}/'
        )
        image_message = random_data['movie_poster']

        keyboard = [
            [
                InlineKeyboardButton(
                    '💿 Добавить в коллекцию', callback_data=f'add_random {random_data["movie_url"]}'
                ),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if len(text_message) > 1024:
            context.bot.send_photo(chat.id, image_message)
            context.bot.send_message(
                chat.id, text_message,
                reply_markup=reply_markup
            )
        else:
            context.bot.send_photo(
                chat.id, image_message,
                caption=text_message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )


def get_data_by_id(update, context, id):
    """Отправка отформатированного сообщения /wisechoice."""
    chat = update.effective_chat
    url_movie_by_id = URL_MOVIE_BY_ID + f'{id}'
    data = {}

    for key, value in get_response(url_movie_by_id).items():
        if value == None:
            data[key] = '-'
        data[key] = value

    if data['movie_type'] == 'tv-series':
        type_url = 'series'
    else:
        type_url = 'film'

    text_message = (
        f'*{data["movie_name"]}* \n'
        f'`Рейтинг: {data["movie_rating"]}` \n'
        f' \n'
        f'*Жанр:* {data["movie_genre"]} '
        f' \n'
        f'_({data["movie_country"]}, '
        f'{data["movie_year"]})_ \n'
        '---- \n'\
        f'{data["movie_description"]} \n'
        f'https://kinopoisk.ru/{type_url}/{data["movie_url"]}/'
    )
    image_message = data['movie_poster']

    # inline button
    keyboard = [
        [
            InlineKeyboardButton(
                '🛋️ Буду смотреть это, удаляй из списка', callback_data=f'del_choiced {id}'
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if len(text_message) > 1024:
        context.bot.send_photo(chat.id, image_message)
        context.bot.send_message(chat.id, text_message, reply_markup=reply_markup)
    else:
        context.bot.send_photo(
            chat.id, image_message,
            caption=text_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
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
    if movie_list == []:
        context.bot.send_message(
            chat.id, 'В коллекции нет фильмов ☹️'
        )
    else:
        random_movie_id = random.choice(movie_list)

        context.bot.send_message(
            chat.id, 'Твой фильм на сегодня:'
        )
        get_data_by_id(update, context, random_movie_id)


def start_add(update, context):
    update.message.reply_text('Отправь мне ссылку на фильм с Кинопоиска:')
    return ADD_MOVIE


def add_movie(update, context):
    chat = update.effective_chat
    
    try:
        url_movie = update.message.text.split('/')
        movie_id = url_movie[-2]

        create_movie_table()
        add_movie_db(chat.id, movie_id)

        url_movie_by_id = URL_MOVIE_BY_ID + f'{movie_id}'

        response = requests.get(url_movie_by_id, headers=HEADERS).json()
        movie_name = response.get('name')

        # inline button
        keyboard = [
            [
                InlineKeyboardButton(
                    '✖️ Отменить добавление', callback_data=f'cancel_add {movie_id}'
                ),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            f'Добавлен фильм "{movie_name}"',
            reply_markup=reply_markup
        )
    except Exception:
        update.message.reply_text(
            f'Не могу найти фильм, возможно ты отправил что-то не то'
        )
    return ConversationHandler.END


def start_del(update, context):
    update.message.reply_text('Отправь мне ссылку на фильм удаления:')
    return DEL_MOVIE


def del_movie(update, context):
    chat = update.effective_chat
    try:
        url_movie = update.message.text.split('/')
        movie_id = url_movie[-2]

        del_movie_db(chat.id, movie_id)

        url_movie_by_id = URL_MOVIE_BY_ID + f'{movie_id}'
        response = requests.get(url_movie_by_id, headers=HEADERS).json()
        movie_name = response.get('name')

        # inline button
        keyboard = [
            [
                InlineKeyboardButton(
                    '✖️ Отменить удаление', callback_data=f'cancel_del {movie_id}'
                ),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            f'Удален фильм "{movie_name}"',
            reply_markup=reply_markup
        )
    except Exception:
        update.message.reply_text(
            f'Не могу найти фильм, возможно ты отправил что-то не то'
        )
    return ConversationHandler.END


def cancel_add(update, context, id):
    chat = update.effective_chat
    movie_id = id

    del_movie_db(chat.id, movie_id)


def cancel_del(update, context, id):
    chat = update.effective_chat
    movie_id = id

    add_movie_db(chat.id, movie_id)


def button(update, context):
    query = update.callback_query
    query.answer()

    choice = query.data
    answer_string = choice.split(' ')
    func_name = answer_string[0]
    movie_id = answer_string[-1]

    if (func_name == 'cancel_del') or (func_name == 'add_random'):
        cancel_del(update, context, movie_id)
        context.bot.edit_message_reply_markup(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=None
        )

    if (func_name == 'cancel_add') or (func_name == 'del_choiced'):
        cancel_add(update, context, movie_id)
        context.bot.edit_message_reply_markup(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=None
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
dispatcher.add_handler(CallbackQueryHandler(button))

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
DEL_MOVIE = 1
dispatcher.add_handler(ConversationHandler(
    entry_points=[CommandHandler('del', start_del)],
    states={
        DEL_MOVIE: [MessageHandler(Filters.text, callback=del_movie)],
    },
    fallbacks=[CommandHandler('quit', quit_conv)]
))


updater.start_polling()
updater.idle()
