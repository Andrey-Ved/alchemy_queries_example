from sqlalchemy import func, distinct
from alchemy_queries_example.db import session_orm
from alchemy_queries_example.models import Genre, Musician, Album, Track, Collection


def queries_printing():
    print('\n1. All albums from 2010:')
    for item in session_orm.query(Album).filter_by(year=2010):
        print(item.name)

    print('\n2. Longest track:')
    for item in session_orm.query(Track). \
            order_by(Track.length.desc()).slice(0, 1):
        print(f'{item.name}, {item.length}')

    print('\n3. Tracks with length not less 3.5min:')
    for item in session_orm.query(Track). \
            filter(180 <= Track.length).order_by(Track.length.desc()):
        print(f'{item.name}, {item.length}')

    print('\n4. Collections between 2011 and 2015 years (inclusive):')
    for item in session_orm.query(Collection). \
            filter(2011 <= Collection.year, Collection.year <= 2015):
        print(item.name)

    print('\n5. Musicians with name that contains not more 1 word:')
    for item in session_orm.query(Musician).filter(Musician.name.notlike('%% %%')):
        print(item.name)

    print('\n6. Tracks that contains word "me" in name:')
    for item in session_orm.query(Track).filter(Track.name.like('%%me%%')):
        print(item.name)
    print('Ok, let\'s start serious work')

    print('\n7. How many musicians plays in each genres:')
    for item in session_orm.query(Genre).join(Genre.musicians). \
            order_by(func.count(Musician.id).desc()).group_by(Genre.id):
        print(f'{item.name}, {len(item.musicians)}')

    print('\n8. How many tracks in all albums 2009-2011:')
    for item in session_orm.query(Track, Album).join(Album). \
            filter(2009 <= Album.year, Album.year <= 2011):
        print(f'{item[0].name}, {item[1].year}')

    print('\n9. Average track length in each album:')
    for item in session_orm.query(Album, func.avg(Track.length)).join(Track). \
            order_by(func.avg(Track.length)).group_by(Album.id):
        print(f'{item[0].name}, {item[1]}')

    print('\n10. All musicians that have no albums in 2010:')
    subquery = session_orm.query(distinct(Musician.name)).join(Musician.albums). \
        filter(Album.year == 2010)

    for item in session_orm.query(distinct(Musician.name)). \
            filter(~Musician.name.in_(subquery)).order_by(Musician.name.asc()):
        print(f'{item}')

    print('\n11. All collections with musician Steve:')
    for item in session_orm.query(Collection). \
            join(Collection.tracks).join(Album).join(Album.musicians). \
            filter(Musician.name == 'Steve').order_by(Collection.name):
        print(f'{item.name}')

    print('\n12. Albums with musicians that play in more than 1 genre:')
    for item in session_orm.query(Album). \
            join(Album.musicians).join(Musician.genres). \
            having(func.count(distinct(Genre.name)) > 1). \
            group_by(Album.id).order_by(Album.name):
        print(f'{item.name}')

    print('\n13. Tracks that not included in any collections:')
    # Important! Despite the warning,
    # following expression does not work: "Collection.id is None"
    for item in session_orm.query(Track).outerjoin(Track.collections). \
            filter(Collection.id == None):
        print(f'{item.name}')

    print('\n14. Musicians with shortest track length:')
    subquery = session_orm.query(func.min(Track.length))

    for item in session_orm.query(Musician, Track.length). \
            join(Musician.albums).join(Track). \
            group_by(Musician.id, Track.length). \
            having(Track.length == subquery.scalar_subquery()).order_by(Musician.name):
        print(f'{item[0].name}, {item[1]}')

    print('\n15. Albums with minimum number of tracks:')
    subquery1 = session_orm.query(func.count(Track.id)). \
        group_by(Track.album_id).order_by(func.count(Track.id)).limit(1)
    subquery2 = session_orm.query(Track.album_id). \
        group_by(Track.album_id).having(func.count(Track.id) == subquery1.scalar_subquery())

    for item in session_orm.query(Album).join(Track). \
            filter(Track.album_id.in_(subquery2)).order_by(Album.name):
        print(f'{item.name}')
