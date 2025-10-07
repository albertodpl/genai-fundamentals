import os
from dotenv import load_dotenv

load_dotenv()

from neo4j import GraphDatabase
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.retrievers import Text2CypherRetriever

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

# Create Cypher LLM
print("Creating OpenAI LLM for text-to-cypher...")
t2c_llm = OpenAILLM(model_name="gpt-4o", model_params={"temperature": 0})
print("✓ Text-to-cypher LLM created")

# Cypher examples as input/query pairs
examples = [
    "USER INPUT: 'Get user ratings for a movie?' QUERY: MATCH (u:User)-[r:RATED]->(m:Movie) WHERE m.title = 'Movie Title' RETURN r.rating"
]

# Specify your own Neo4j schema
neo4j_schema = """
Node properties:
Person {name: STRING, born: INTEGER}
Movie {tagline: STRING, title: STRING, released: INTEGER}
Genre {name: STRING}
User {name: STRING}

Relationship properties:
ACTED_IN {role: STRING}
RATED {rating: INTEGER}

The relationships:
(:Person)-[:ACTED_IN]->(:Movie)
(:Person)-[:DIRECTED]->(:Movie)
(:User)-[:RATED]->(:Movie)
(:Movie)-[:IN_GENRE]->(:Genre)
"""

# Build the retriever
print("Creating Text2Cypher retriever...")
retriever = Text2CypherRetriever(
    driver=driver,
    llm=t2c_llm,
    neo4j_schema=neo4j_schema,
    examples=examples,
)
print("✓ Retriever created")

print("Creating OpenAI LLM for generation...")
llm = OpenAILLM(model_name="gpt-4o")
print("✓ Generation LLM created")

print("Creating GraphRAG pipeline...")
rag = GraphRAG(retriever=retriever, llm=llm)
print("✓ GraphRAG pipeline created")

query_text = "Which movies did Hugo Weaving star in?"
print(f"Executing GraphRAG search with query: '{query_text}'...")
response = rag.search(query_text=query_text, return_context=True)
print("✓ Search complete")

print("\nAnswer:")
print(response.answer)
print("\nCYPHER :", response.retriever_result.metadata["cypher"])
print("\nCONTEXT:", response.retriever_result.items)

driver.close()
print("\n✓ Database connection closed")
