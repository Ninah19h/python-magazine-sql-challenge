from .database_utils import get_connection
# import the function to get a database connection

class Author:
    def __init__(self, name: str, id: int = None):
        # initialize an author with name and optional id
        # check that name is a non-empty string
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        self._name = name.strip()
        self.id = id  # set id if provided

    @property
    def name(self) -> str:
        # getter for author name
        return self._name

    @classmethod
    def new_from_db(cls, row):
        # create an author object from a database row
        if not row:
            return None
        # support sqlite3.Row (mapping) and tuple rows
        try:
            _id = row["id"]
            _name = row["name"]
        except Exception:
            _id = row[0]
            _name = row[1]
        return cls(_name, id=_id)

    @classmethod
    def find_by_id(cls, id: int):
        # find an author by id in the database
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None

    def save(self):
        # save the author to the database
        conn = get_connection()
        cur = conn.cursor()
        if self.id:
            # update existing author
            cur.execute("UPDATE authors SET name = ? WHERE id = ?", (self._name, self.id))
        else:
            # insert new author
            cur.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
            self.id = cur.lastrowid  # set the new id
        conn.commit()
        conn.close()

    #relationships
    def articles(self):
        # return all articles written by this author
        from .article import Article  # local import to avoid circular import
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Article.new_from_db(r) for r in rows]

    def magazines(self):
        # return all distinct magazines where this author has articles
        from .magazine import Magazine  # local import to avoid circular import
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            select distinct m.* from magazines m
            join articles a on a.magazine_id = m.id
            where a.author_id = ?
            """,
            (self.id,),
        )
        rows = cur.fetchall()
        conn.close()
        return [Magazine.new_from_db(r) for r in rows]

    #phase4 methods 
    def add_article(self, magazine, title):
        """create and save an article with this author and the given magazine"""
        from .article import Article
        from .magazine import Magazine

        if not isinstance(magazine, Magazine):
            raise ValueError("magazine must be a magazine instance")
        article = Article(title, self, magazine)
        article.save()  # save the article to db
        return article

    def topic_areas(self):
        """return unique categories from the magazines this author has articles in"""
        mags = self.magazines()
        seen = []
        for m in mags:
            if m.category not in seen:
                seen.append(m.category)  # collect unique categories
        return seen
