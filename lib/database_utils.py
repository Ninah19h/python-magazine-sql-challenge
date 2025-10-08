import sqlite3 # import sqlite3 to work with sqlite databases  
#from typing import Optional

DB_FILE = "magazine.db"
# set the database file name

def get_connection() -> sqlite3.Connection:
    """return a sqlite3 connection with row factory set to sqlite3.row"""
    conn = sqlite3.connect(DB_FILE)  # connect to the database file
    conn.row_factory = sqlite3.Row  # rows can be accessed like dictionaries
    return conn

def create_tables() -> None:
    """enable foreign keys and create the authors, magazines, and articles tables"""
    conn = get_connection()  # open database connection
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")  # enable foreign key support

    # create authors table if it doesn't exist
    cur.execute(
        """
        create table if not exists authors (
            id integer primary key autoincrement,
            name text not null
        );
        """
    )

    # create magazines table if it doesn't exist
    cur.execute(
        """
        create table if not exists magazines (
            id integer primary key autoincrement,
            name text not null,
            category text not null
        );
        """
    )

    # create articles table if it doesn't exist
    cur.execute(
        """
        create table if not exists articles (
            id integer primary key autoincrement,
            title text not null,
            author_id integer not null,
            magazine_id integer not null,
            foreign key (author_id) references authors(id) on delete cascade,
            foreign key (magazine_id) references magazines(id) on delete cascade
        );
        """
    )

    conn.commit()  # save changes to db
    conn.close()  # close db connection
