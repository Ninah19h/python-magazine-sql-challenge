import pytest
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article
from lib.database_utils import create_tables

#to ensure tables exist
create_tables()

def test_author_save_and_find():
    a = Author("Test Author")
    a.save()
    found = Author.find_by_id(a.id)
    assert found.name == "Test Author"

def test_magazine_save_and_find():
    m = Magazine("Test Magazine", "Test Category")
    m.save()
    found = Magazine.find_by_id(m.id)
    assert found.name == "Test Magazine"
    assert found.category == "Test Category"

def test_article_save_and_relationships():
    a = Author("Article Author")
    a.save()
    m = Magazine("Article Magazine", "Articles")
    m.save()
    art = Article("Test Article", a, m)
    art.save()

    assert art.title == "Test Article"
    # Test relationships
    assert art.author.name == "Article Author"
    assert art.magazine.name == "Article Magazine"

#phase4 nd the bonus tests

from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article
from lib.database_utils import create_tables

#tables exist
create_tables()

def test_add_article_and_topic_areas():
    #create author and magazine
    a = Author("Phase4 Author")
    a.save()
    m1 = Magazine("Tech Mag", "Technology")
    m1.save()
    m2 = Magazine("Health Mag", "Health")
    m2.save()

    #add articles using add_article
    art1 = a.add_article(m1, "Tech Article 1")
    art2 = a.add_article(m2, "Health Article 1")

    #check that articles are saved correctly
    assert art1.title == "Tech Article 1"
    assert art2.title == "Health Article 1"

    # Check topic areas are unique
    topics = a.topic_areas()
    assert "Technology" in topics
    assert "Health" in topics
    assert len(topics) == 2

def test_magazine_article_titles_and_contributors():
    # Create author and magazine
    a1 = Author("Contributor One")
    a1.save()
    a2 = Author("Contributor Two")
    a2.save()
    m = Magazine("Science Mag", "Science")
    m.save()

    # Add multiple articles
    a1.add_article(m, "Science Article 1")
    a1.add_article(m, "Science Article 2")
    a1.add_article(m, "Science Article 3")
    a2.add_article(m, "Science Article 4")  # only 1 article

    # Test article_titles
    titles = m.article_titles()
    assert "Science Article 1" in titles
    assert "Science Article 4" in titles
    assert len(titles) == 4

    # Test contributing_authors (>2 articles)
    contribs = m.contributing_authors()
    names = [c.name for c in contribs]
    assert "Contributor One" in names
    assert "Contributor Two" not in names  # only one article

def test_top_publisher():
    # Create magazines and authors
    m1 = Magazine("Mag A", "Category A")
    m1.save()
    m2 = Magazine("Mag B", "Category B")
    m2.save()
    a = Author("Top Author")
    a.save()

    # Add articles to magazines
    for i in range(5):
        a.add_article(m1, f"Article {i+1}")
    for i in range(3):
        a.add_article(m2, f"Article B{i+1}")

    # Top publisher should be m1
    top = Magazine.top_publisher()
    assert top.name == "Mag A"
