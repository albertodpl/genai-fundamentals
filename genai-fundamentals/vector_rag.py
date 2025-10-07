import os

from neo4j import GraphDatabase
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
from neo4j_graphrag.retrievers import VectorRetriever
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.generation import GraphRAG

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

# Create retriever
print("Creating vector retriever...")
retriever = VectorRetriever(
    driver,
    index_name="moviePlots",
    embedder=embedder,
    return_properties=["title", "plot"],
)
print("✓ Retriever created")

# Create the LLM
print("Creating OpenAI LLM...")
llm = OpenAILLM(model_name="gpt-4o")
print("✓ LLM created")

# Create GraphRAG pipeline
print("Creating GraphRAG pipeline...")
rag = GraphRAG(retriever=retriever, llm=llm)
print("✓ GraphRAG pipeline created")

# Search
query_text = "Find me movies about toys coming alive"
print(f"Executing GraphRAG search with query: '{query_text}'...")
response = rag.search(query_text=query_text, retriever_config={"top_k": 5})
print("✓ Search complete")

print("\nAnswer:")
print(response.answer)

# CLose the database connection
driver.close()
print("\n✓ Database connection closed")
