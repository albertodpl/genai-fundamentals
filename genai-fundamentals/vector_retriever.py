import os

from neo4j import GraphDatabase
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
from neo4j_graphrag.retrievers import VectorRetriever

from dotenv import load_dotenv

print("✓ Imports successful")

load_dotenv()
print("✓ Environment loaded")

# Connect to Neo4j database
print(f"Attempting to connect to Neo4j at {os.getenv('NEO4J_URI')}...")
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")),
)
print("✓ Driver created")

# Test the connection
try:
    driver.verify_connectivity()
    print("✓ Connection verified")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit(1)

# Create embedder
print("Creating OpenAI embedder...")
embedder = OpenAIEmbeddings(model="text-embedding-ada-002")
print("✓ Embedder created")

# Test embedder separately
print("Testing embedder with sample text...")
test_embedding = embedder.embed_query("test")
print(f"✓ Embedder works, vector length: {len(test_embedding)}")

# Create retriever
print("Creating vector retriever...")
retriever = VectorRetriever(
    driver,
    index_name="moviePlots",
    embedder=embedder,
    return_properties=["title", "plot"],
)
print("✓ Retriever created")

# Search for similar items
print("Executing search (this will call OpenAI API)...")
result = retriever.search(query_text="Toys coming alive", top_k=5)
print(f"✓ Search complete, got {len(result.items)} results")

# Parse results
for item in result.items:
    print(item.content, item.metadata["score"])

# CLose the database connection
driver.close()
print(f"✓ Search complete, got {len(result.items)} results")
