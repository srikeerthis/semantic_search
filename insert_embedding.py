# insert_embedding.py
import warnings
warnings.filterwarnings("ignore", message=".*clean_up_tokenization_spaces.*")

import psycopg2
from transformers import AutoTokenizer, AutoModel
import torch

# Load the pre-trained transformer model for embeddings
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Function to generate embeddings for a given text
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding

# Function to insert a document and its embedding into the PostgreSQL database
def insert_document(text):
    # Generate the embedding for the given text
    embedding = get_embedding(text)

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="your_new_db",
        user="search_assistant",
        password="search@123",
        host="localhost"
    )
    cur = conn.cursor()

    # Insert the document and its embedding into the database
    cur.execute(
        "INSERT INTO documents (text, embedding) VALUES (%s, %s)",
        (text, embedding.tolist())  # Convert the embedding to a list
    )

    # Commit the transaction and close the connection
    conn.commit()
    cur.close()
    conn.close()

# Example usage (you can remove or modify this based on your needs)
if __name__ == "__main__":
    # Example documents
    documents = [
        "Artificial intelligence is transforming the world of technology.",
        "Machine learning is a subset of artificial intelligence that focuses on learning from data.",
        "Natural language processing is a branch of AI that helps computers understand human language.",
        "Self-driving cars are one of the most exciting applications of machine learning.",
        "AI in healthcare is being used to diagnose diseases and suggest treatments.",
        "Deep learning is a specialized form of machine learning with multiple layers of neural networks."
    ]

    # Insert these documents
    for doc in documents:
        insert_document(doc)

