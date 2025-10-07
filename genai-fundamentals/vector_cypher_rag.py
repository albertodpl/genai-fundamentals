import os
from dotenv import load_dotenv

load_dotenv()

from neo4j import GraphDatabase
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.retrievers import VectorCypherRetriever

print("✓ Imports successful")
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

# Define retrieval query
retrieval_query = """
MATCH (node)<-[r:RATED]-()
RETURN 
  node.title AS title, node.plot AS plot, score AS similarityScore, 
  collect { MATCH (node)-[:IN_GENRE]->(g) RETURN g.name } as genres, 
  collect { MATCH (node)<-[:ACTED_IN]->(a) RETURN a.name } as actors, 
  avg(r.rating) as userRating
ORDER BY userRating DESC
"""

# Create retriever
print("Creating vector cypher retriever...")
retriever = VectorCypherRetriever(
    driver,
    index_name="moviePlots",
    embedder=embedder,
    retrieval_query=retrieval_query,
)
print("✓ Retriever created")

#  Create the LLM
print("Creating OpenAI LLM...")
llm = OpenAILLM(model_name="gpt-4o")
print("✓ LLM created")

# Create GraphRAG pipeline
print("Creating GraphRAG pipeline...")
rag = GraphRAG(retriever=retriever, llm=llm)
print("✓ GraphRAG pipeline created")

# Search
query_text = "Find the highest rated action movie about travelling to other planets"
print(f"Executing GraphRAG search with query: '{query_text}'...")
response = rag.search(
    query_text=query_text, retriever_config={"top_k": 5}, return_context=True
)
print("✓ Search complete")

print("\nAnswer:")
print(response.answer)
print("\nCONTEXT:", response.retriever_result.items)

# Close the database connection
driver.close()
print("\n✓ Database connection closed")

