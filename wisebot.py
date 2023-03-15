from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

from telegram import ReplyKeyboardMarkup, ParseMode

import requests

KP_TOKEN = '66XDW7D-CT0MF9Z-GZB7XYF-65WAXFN'
KP_KEY = 'X-API-KEY'
URL_RANDOM = 'https://api.kinopoisk.dev/v1/movie/random'
HEADERS = {KP_KEY: KP_TOKEN}
updater = Updater(token='5902172202:AAHewEIuOCNWpnyfWyVkiY1o7i8RlJrXFKU')


def get_response_random():
    """Получение словаря данных о фильме."""
    response = requests.get(URL_RANDOM, headers=HEADERS).json()
    random_data_fields = {
        'random_movie_name': response.get('name'),
        'random_movie_rating': response.get('rating').get('kp'),
        'random_movie_year': response.get('year'),
        'random_movie_country': response.get('countries')[0].get('name'),
        'random_movie_description': response.get('description'),
        'random_movie_poster': response.get('poster').get('url'),
        'random_movie_url': response.get('id'),
        'random_movie_type': response.get('type')
    }
    return random_data_fields


def get_data_random(update, context):
    """Отправка отформатированного сообщения."""
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
    text_message = (
        f'*{random_data["random_movie_name"]}*. '\
        f'Рейтинг: {random_data["random_movie_rating"]}. '\
        f'Страна: {random_data["random_movie_country"]}. '\
        f'Год: {random_data["random_movie_year"]}. \n'\
        '---- \n'\
        f'Описание: {random_data["random_movie_description"]} \n'\
        f'https://kinopoisk.ru/{type_url}/{random_data["random_movie_url"]}/'
    )
    image_message = random_data['random_movie_poster']
    
    context.bot.send_photo(chat.id, image_message)
    context.bot.send_message(
        chat.id, text_message, parse_mode=ParseMode.MARKDOWN
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
        'random - получить два случайных фильма из КП \n'
        'wisechoice - выбрать случайный фильм из своего списка \n'
        'add - добавить фильм в коллекцию (ссылка должна быть с КП) \n'
        'del - удалить фильм из коллекции (ссылка должна быть с КП) \n'
    )
    button = ReplyKeyboardMarkup([
        ['/random', '/wisechoice'],
        ['/add', '/del']
    ], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо за доверие в выборе, {name}')
    context.bot.send_message(
        chat_id=chat.id,
        text=text,
        reply_markup=button
    )


def wisechoice(update, context):
    chat = update.effective_chat
    text_message = '_Функция пока в разработке_'
    context.bot.send_message(
        chat.id, text_message, parse_mode=ParseMode.MARKDOWN
    )


def add_movie(update, context):
    chat = update.effective_chat
    text_message = '_Функция пока в разработке_'
    context.bot.send_message(
        chat.id, text_message, parse_mode=ParseMode.MARKDOWN
    )


def del_movie(update, context):
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
