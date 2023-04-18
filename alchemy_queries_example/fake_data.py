from random import choice, randint


names = [
    'Смирнов Максим',
    'Бондарева Злата',
    # 'Гусева Ника',
    # 'Васильев Али',
    # 'Коновалова Анастасия',
    # 'Иванова Амалия',
    # 'Петров Даниил',
    'Зайцева Анна'
]

genres = [
    'Фолк-музыка',
    'Кантри',
    'Ритм-н-блюз',
    'Джаз',
    'Шансон'
]

years = [
    2008,
    2009,
    2010,
    2011
]


def create_fake_data(db_size=30, collections_number=2):

    genres_musicians = {}

    for musician in names:
        genres_musicians[musician] = [choice(genres) for _ in range(3)]

    data = []
    albums = {}
    collections_year = {}

    for record_id in range(db_size):

        row = {
            'track': f'track{record_id}',
            'musician': choice(names)
        }

        row['genre'] = choice(genres_musicians[row['musician']])

        if row['musician'] + row['genre'] not in albums:
            albums[row['musician'] + row['genre']] = f'albom {len(albums) + 1}'

        row['album'] = albums[row['musician'] + row['genre']]

        row['collection'] = f'collection{randint(1, collections_number)}'

        if row['collection'] not in collections_year:
            collections_year[row['collection']] = choice(years)

        row['collection_year'] = collections_year[row['collection']]

        row['length'] = randint(30, 300)

        data.append(row)

    return data
