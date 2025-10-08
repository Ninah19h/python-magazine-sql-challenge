from .database_utils import get_connection
# import the function to get a database connection

class Magazine:
    def __init__(self, name: str, category: str, id: int = None):
        # initialize a magazine with name, category, and optional id
        self.name = name  # uses setter for validation
        self.category = category  # uses setter for validation
        self.id = id

    @property
    def name(self) -> str:
        # getter for magazine name
        return self._name

    @name.setter
    def name(self, value: str):
        # setter with validation for magazine name
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string.")
        self._name = value.strip()

    @property
    def category(self) -> str:
        # getter for magazine category
        return self._category

    @category.setter
    def category(self, value: str):
        # setter with validation for magazine category
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Category must be a non-empty string.")
        self._category = value.strip()

    @classmethod
    def new_from_db(cls, row):
        # create a magazine object from a database row
        if not row:
            return None
        try:
            _id = row["id"]
            _name = row["name"]
            _category = row["category"]
        except Exception:
            _id = row[0]
            _name = row[1]
            _category = row[2]
        return cls(_name, _category, id=_id)

    @classmethod
    def find_by_id(cls, id: int):
        # find a magazine by id in the database
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None

    def save(self):
        # save the magazine to the database
        conn = get_connection()
        cur = conn.cursor()
        if self.id:
            # update existing magazine
            cur.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self._name, self._category, self.id),
            )
        else:
            # insert new magazine
            cur.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self._name, self._category),
            )
            self.id = cur.lastrowid  # set new id after insertion
        conn.commit()
        conn.close()

    def articles(self):
        # return all articles in this magazine
        from .article import Article
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Article.new_from_db(r) for r in rows]

    def contributors(self):
        # return all authors who have articles in this magazine
        from .author import Author
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            select distinct a.* from authors a
            join articles ar on ar.author_id = a.id
            where ar.magazine_id = ?
            """,
            (self.id,),
        )
        rows = cur.fetchall()
        conn.close()
        return [Author.new_from_db(r) for r in rows]

    def article_titles(self):
        # return a list of titles for articles in this magazine
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cur.fetchall()
        conn.close()
        titles = []
        for r in rows:
            try:
                titles.append(r["title"])
            except Exception:
                titles.append(r[0])
        return titles

    def contributing_authors(self):
        # return authors with more than 2 articles in this magazine
        from .author import Author
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            select a.* from authors a
            join articles ar on ar.author_id = a.id
            where ar.magazine_id = ?
            group by a.id
            having count(ar.id) > 2
            """,
            (self.id,),
        )
        rows = cur.fetchall()
        conn.close()
        return [Author.new_from_db(r) for r in rows]

    @classmethod
    def top_publisher(cls):
        # return the magazine with the most articles
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            select m.*, count(a.id) as cnt
            from magazines m
            left join articles a on a.magazine_id = m.id
            group by m.id
            order by cnt desc
            limit 1
            """
        )
        row = cur.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None
