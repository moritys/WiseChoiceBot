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
    # сделать проверку если фильмов нет == 0
    # брать только фильмы этого юзера
    # после вывода добавить предложение удалить фильм (кнопка под сообщением)
    chat = update.effective_chat
    text_message = '_Функция пока в разработке_'
    context.bot.send_message(
        chat.id, text_message, parse_mode=ParseMode.MARKDOWN
    )


def add_movie(update, context):
    # проверка на ссылку
    # отрезать тип фильма
    # отрезать айди фильма
    # сохранить под определенным юзером
    chat = update.effective_chat
    text_message = (
        'Чтобы добавить фильм себе в коллекцию, '
        'отправь мне ссылку с Кинопоиска'
    )
    context.bot.send_message(
        chat.id, text_message, parse_mode=ParseMode.MARKDOWN
    )
    message_from_user = context.message.text
    context.bot.send_message(
        chat.id, message_from_user, parse_mode=ParseMode.MARKDOWN
    )


def get_movie(update, context):
    pass


def del_movie(update, context):
    # проверить есть ли этот фильм в списке
    # удалить фильм из базы
    # добавить кнопку восстановления
    chat = update.effective_chat
    text_message = '_Функция пока в разработке_'
    context.bot.send_message(
        chat.id, text_message, parse_mode=ParseMode.MARKDOWN
    )


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('random', new_random))
updater.dispatcher.add_handler(CommandHandler('wisechoice', wisechoice))
updater.dispatcher.add_handler(CommandHandler('add', add_movie))
updater.dispatcher.add_handler(CommandHandler('del', del_movie))

updater.start_polling()
updater.idle()
