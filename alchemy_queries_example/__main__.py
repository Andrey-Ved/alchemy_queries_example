from alchemy_queries_example.fake_data import create_fake_data
from alchemy_queries_example.filling import filling_db
from alchemy_queries_example.queries import queries_printing


def main():
    data = create_fake_data(
        db_size=10,
        collections_number=2
    )

    for i in range(len(data)):
        print(data[i])

    filling_db(data)

    queries_printing()


if __name__ == '__main__':
    main()