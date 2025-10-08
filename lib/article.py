from .database_utils import get_connection
#import the function to get a database connection

class Article:
    def __init__(self, title, author, magazine):
        # initialize an article object with title, author, and magazine
        # ensure title is a non-empty string
        if not isinstance(title, str) or len(title.strip()) == 0:
            raise ValueError("Title must be a non-empty string.")
        self._title = title.strip()
        self.author = author
        self.magazine = magazine
        self.id = None  # id will be set when saved to db

    @property
    def title(self):
        # getter for the article title
        return self._title

    @classmethod
    def new_from_db(cls, row):
        # create an article object from a database row
        from .author import Author
        from .magazine import Magazine
        author = Author.find_by_id(row[3])  # get author object using id from row
        magazine = Magazine.find_by_id(row[4])  # get magazine object using id from row
        art = cls(row[1], author, magazine)  # create article instance
        art.id = row[0]  # set the article id from db
        return art

    def save(self):
        # save the article to the database
        conn = get_connection()  # open db connection
        cursor = conn.cursor()
        if self.id:
            # if article already exists, update it
            cursor.execute(
                "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self._title, self.author.id, self.magazine.id, self.id)
            )
        else:
            # if article is new, insert it
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self._title, self.author.id, self.magazine.id)
            )
            self.id = cursor.lastrowid  # set the new id after insertion
        conn.commit()  # commit changes to db
        conn.close()  # close db connection
