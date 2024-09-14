# Semantic Search using Postgres database

This project is a simple Flask-based web application that allows users to insert documents into a PostgreSQL database, and perform semantic searches based on text embeddings. The search functionality is powered by a pre-trained transformer model, and results are retrieved based on similarity to the search query.

## Features

- Insert multiple documents into the database.
- Perform semantic search using a query to find similar documents.
- Display search results on the same page as the search form.
- Navigation bar for easy access between the home page (search) and the insert page.

## Tech Stack

- **Backend**: Flask, Python
- **Database**: PostgreSQL with `pgvector` extension for storing embeddings.
- **Machine Learning Model**: Hugging Face's `sentence-transformers/all-MiniLM-L6-v2` for generating text embeddings.
- **Frontend**: HTML (rendered by Flask templates).

## Prerequisites

1. **Python 3.7+**
2. Install dependencies: 
    ```
    pip install Flask psycopg2 transformers torch
    ```

2. **PostgreSQL** installed with the `pgvector` extension:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
## Setup
1. Clone the Repository
    ```
    git clone https://github.com/your-repository/flask-semantic-search.git
    cd flask-semantic-search
    ```
2. Setup PostgreSQL Database
    Create a new PostgreSQL database:
    ```
    CREATE DATABASE your_new_db;
    ```
    Create a table for storing documents and embeddings:
    ```
    CREATE TABLE documents (
        id SERIAL PRIMARY KEY,
        text TEXT,
        embedding VECTOR(384)  -- Adjust to the size of your embedding model
    );
    ```
3. Configure the Database Connection

    Edit the database connection details in app.py:
    ```
    def get_db_connection():
    conn = psycopg2.connect(
        dbname="your_new_db",
        user="your_username",
        password="your_password",
        host="localhost"
    )
    return conn
    ```

4. Run the Flask App
    ```
    python app.py
    ```

The app will be available at http://localhost:5000/.

## Usage
Inserting Documents

    Navigate to the Insert Documents page (http://localhost:5000/insert).
    Enter multiple documents, one per line, in the provided form.
    Click "Insert Documents" to add them to the database.

Performing a Search

    Go to the Home page (http://localhost:5000/).
    Enter a search query in the search bar.
    Click "Search" to view similar documents based on the query.

Example
Sample Document:
```
Artificial intelligence (AI) is a field of computer science that aims to create systems capable of performing tasks that typically require human intelligence. These tasks include visual perception, speech recognition, decision-making, and language translation.
```

Sample Query:

    Query: "What is artificial intelligence?"
    Expected Result: The document about AI should be returned due to its relevance to the query.

## License
This project is licensed under the MIT License.
