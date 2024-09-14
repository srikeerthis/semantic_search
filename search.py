# search.py

import warnings
warnings.filterwarnings("ignore", message=".*clean_up_tokenization_spaces.*")
import psycopg2
from insert_embedding import get_embedding  # Reuse the get_embedding function
from dotenv import load_dotenv
import os

load_dotenv()

# Function to search for similar documents based on a query
def search_similar_documents(query, top_k=5):
    # Generate the embedding for the query
    query_embedding = get_embedding(query)

    # Convert the embedding to a string format suitable for PostgreSQL
    query_embedding_str = '[' + ','.join(map(str, query_embedding.tolist())) + ']'

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=os.getenv("dbname"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host")
    )
    cur = conn.cursor()

    # SQL query to find the top-k most similar documents using cosine distance
    cur.execute(f"""
        SELECT id, text, embedding <=> '{query_embedding_str}'::vector AS distance
        FROM documents
        ORDER BY embedding <=> '{query_embedding_str}'::vector
        LIMIT %s
    """, (top_k,))

    # Fetch the results
    results = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Check if results were found
    if len(results) == 0:
        print("No similar documents found.")
    else:
        # Return the results if found
        return results

# Example usage
if __name__ == "__main__":
    query_text = "How is AI used in healthcare?"
    results = search_similar_documents(query_text)

    # Print the results or notify if no documents were found
    if results:
        for result in results:
            print(f"Document ID: {result[0]}, Text: {result[1]}, Distance: {result[2]}")
