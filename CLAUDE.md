# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About This Repository

Learning repository for the Neo4j & Generative AI Fundamentals course from GraphAcademy. It demonstrates various RAG (Retrieval-Augmented Generation) patterns using Neo4j and OpenAI.

## Environment Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

1. Copy `.env.example` to `.env` and populate with credentials:
   - `OPENAI_API_KEY`: OpenAI API key
   - `NEO4J_URI`: Neo4j connection URI
   - `NEO4J_USERNAME`: Neo4j username (typically "neo4j")
   - `NEO4J_PASSWORD`: Neo4j password

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Verify environment setup:
   ```bash
   uv run genai-fundamentals/test_environment.py
   ```

## Architecture

The repository is structured around teaching RAG implementations with Neo4j:

### Core Patterns

1. **Vector RAG** (`vector_rag.py`): Basic vector similarity search using embeddings
   - Uses `VectorRetriever` with OpenAI embeddings
   - Searches against `moviePlots` vector index
   - Returns matched documents based on semantic similarity

2. **Vector + Cypher RAG** (`vector_cypher_rag.py`): Vector search enhanced with graph traversal
   - Combines vector similarity with graph relationships
   - Uses custom Cypher query to enrich results (genres, actors, ratings)
   - Provides richer context by traversing graph connections

3. **Text-to-Cypher RAG** (`text2cypher_rag.py`): Natural language to graph query
   - Uses `Text2CypherRetriever` to convert questions to Cypher queries
   - LLM generates Cypher from natural language
   - Direct graph querying without embeddings

### Directory Structure

- `genai-fundamentals/`: Main module with skeleton/exercise files (incomplete implementations)
- `genai-fundamentals/solutions/`: Complete, working implementations
- `conftest.py`: pytest configuration and test helpers (loads `.env`, provides test utilities)

### Key Dependencies

- `neo4j-graphrag[openai]`: Neo4j's GraphRAG library with OpenAI integration
- `neo4j`: Neo4j Python driver
- `openai`: OpenAI API client
- `python-dotenv`: Environment variable management

## Common Commands

### Testing

Run all solution tests:
```bash
uv run pytest genai-fundamentals/solutions
```

Run specific test:
```bash
uv run pytest genai-fundamentals/solutions/test_solutions.py::test_vector_rag
```

Run environment verification:
```bash
uv run genai-fundamentals/test_environment.py
```

### Running Examples

Execute solution files directly:
```bash
uv run -m genai-fundamentals.solutions.vector_rag
uv run -m genai-fundamentals.solutions.text2cypher_rag
uv run -m genai-fundamentals.solutions.vector_cypher_rag
```

## Neo4j Database Prerequisites

The code expects a Neo4j instance with:
- The `recommendations` dataset loaded
- Vector embeddings added to movie plot data
- A vector index named `moviePlots` created

Setup instructions: https://github.com/neo4j-graphacademy/courses/blob/main/asciidoc/courses/genai-fundamentals/modules/2-rag/lessons/3-vector-index/reset.cypher

## Testing Framework

`conftest.py` provides `TestHelpers` class with:
- `run_module()`: Executes Python modules and captures output (for testing exercises)
- `run_cypher()`: Executes Cypher queries against Neo4j
- Auto-loads `.env` file for all tests via fixture
