from sqlalchemy import and_

from alchemy_queries_example.db import session_orm
from alchemy_queries_example.models import Genre, Musician, Album, Track, Collection


def filling_db(data):
    print('\nPreparing data for ORM job...')
    count = 0

    for item in data:
        count += 1

        genre = session_orm.query(Genre).filter_by(
            name=item['genre']
        ).scalar()

        if not genre:
            genre = Genre(
                name=item['genre']
            )

        session_orm.add(genre)

        musician = session_orm.query(Musician).filter_by(
            name=item['musician']
        ).scalar()

        if not musician:
            musician = Musician(
                name=item['musician']
            )

        musician.genres.append(genre)
        session_orm.add(musician)

        album = session_orm.query(Album).filter_by(
            name=item['album']
        ).scalar()

        if not album:
            album = Album(
                name=item['album'],
                year=item['collection_year']
            )

        album.musicians.append(musician)
        session_orm.add(album)

        track = session_orm.query(Track).join(Album).filter(
            and_(
                Track.name == item['track'],
                Album.name == item['album']
            )
        ).scalar()

        if not track:
            track = Track(
                name=item['track'],
                length=item['length']
            )

        track.album_id = album.id
        session_orm.add(track)

        if item['collection']:
            collection = session_orm.query(Collection).filter_by(
                name=item['collection']
            ).scalar()

            if not collection:
                collection = Collection(
                    name=item['collection'],
                    year=item['collection_year']
                )

            collection.tracks.append(track)
            session_orm.add(collection)

        session_orm.commit()
