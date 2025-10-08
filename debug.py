from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article
from lib.database_utils import create_tables

create_tables()

# Create and save an author
author1 = Author("Jerolinah")
author1.save()

# Create and save a magazine
mag1 = Magazine("Tech World", "Technology")
mag1.save()

# Create and save an article
article1 = Article("The Future of Smart Homes", author1, mag1)
article1.save()


print("No errors everything is  successfully!")
