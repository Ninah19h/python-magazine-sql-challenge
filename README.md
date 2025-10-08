# Object Relations Code Challenge - Articles
# Python Magazine SQL Challenge

## Project Overview
This project is a Python application that models a simple magazine publishing system. It uses **SQLite** as the database and raw SQL for CRUD operations.

The main entities are:
- **Author**: Represents an author who writes articles.
- **Magazine**: Represents a magazine that publishes articles.
- **Article**: Represents an article written by an author and published in a magazine.

## Features
- **Database Schema**: Creates tables for authors, magazines, and articles with proper foreign key constraints.
- **CRUD Operations**: Create, read, update, and save authors, magazines, and articles.
- **Relationships**:
  - Author ↔ Articles ↔ Magazines
  - Magazine ↔ Articles ↔ Authors
- **Aggregate Methods** (Phase 4):
  - `add_article` (Author)
  - `topic_areas` (Author)
  - `article_titles` (Magazine)
  - `contributors` and `contributing_authors` (Magazine)
  - `top_publisher` (Magazine)

## Project Structure
├── venv/ # Virtual environment (ignored by Git)
├── lib/
│ ├── init.py
│ ├── author.py
│ ├── magazine.py
│ ├── article.py
│ └── database_utils.py
├── tests/
│ ├── init.py
│ └── test_all.py
├── debug.py
├── .gitignore
└── requirements.txt

# Setup Instructions
Clone the repo
# creating  and activate virtual environment
python3 -m venv venv
source venv/bin/activate   (Linux)

# installing  dependencies
pip install -r requirements.txt
   


# final steps
python debug.py

# run test
pytest


