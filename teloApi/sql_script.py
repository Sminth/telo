from .connect import get_db

from flask import g


def create_table():
    # get_db().execute("DROP TABLE personnel IF EXISTS")
    get_db().execute("""
        CREATE TABLE personnel(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom VARCHAR(50),
            prenoms VARCHAR(50),
            contact VARCHAR(50),
            photo VARCHAR(50),
            poste VARCHAR(50),
            description VARCHAR(50),
            done BOOLEAN,
            section VARCHAR(50),
            section_image VARCHAR(50),
        )
    """)

if __name__ == '__main__':
    create_table()
