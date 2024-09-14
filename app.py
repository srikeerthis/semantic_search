from flask import Flask, request, jsonify, render_template
import psycopg2
from transformers import AutoTokenizer, AutoModel
import torch

app = Flask(__name__)

# Load the pre-trained transformer model for embeddings
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Function to generate embeddings
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding

# Connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        dbname="your_new_db",
        user="search_assistant",
        password="search@123",
        host="localhost"
    )
    return conn

@app.route('/insert', methods=['GET', 'POST'])
def insert_documents():
    if request.method == 'POST':
        # Handle form submission and insert documents
        content = request.form['content']
        documents = content.splitlines()  # Split the input by line breaks to get multiple documents
        
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert each document with its embedding
        for document in documents:
            if document.strip():  # Only process non-empty lines
                embedding = get_embedding(document)
                cur.execute(
                    "INSERT INTO documents (text, embedding) VALUES (%s, %s)",
                    (document, embedding.tolist())
                )
        
        conn.commit()
        cur.close()
        conn.close()

        return render_template('insert.html', message="Documents inserted successfully!")

    # If it's a GET request, show the form
    return render_template('insert.html')


# Home route (for the search page and results)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form.get('query')
        if not query:
            return render_template('index.html', message="No query provided.")
        
        # Generate the embedding for the query
        query_embedding = get_embedding(query)
        query_embedding_str = '[' + ','.join(map(str, query_embedding.tolist())) + ']'

        # Connect to the PostgreSQL database and search for similar documents
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(f"""
            SELECT id, text, embedding <=> '{query_embedding_str}'::vector AS distance
            FROM documents
            ORDER BY embedding <=> '{query_embedding_str}'::vector
            LIMIT 5
        """)

        results = cur.fetchall()
        cur.close()
        conn.close()

        # If no results are found, render the same page with a message
        if len(results) == 0:
            return render_template('index.html', query=query, message="No similar documents found.")

        # Render the page with search results
        return render_template('index.html', query=query, results=results)
    
    # If it's a GET request, just render the search form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
