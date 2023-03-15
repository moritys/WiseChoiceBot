from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

random_data_fields = {
    'random_movie_name': 'name',
    'random_movie_rating': 'rating',
    'random_movie_description': 'description',
    'random_movie_poster': 'poster',
}

for data, value in random_data_fields.items():
    new_data = data
    new_value = value
    print(f'{new_data}: {new_value}')