# Setup

This repository accompanies the [Neo4j and GenerativeAI Fundamentals course](https://graphacademy.neo4j.com/courses/genai-fundamentals) on [GraphAcademy](https://graphacademy.neo4j.com).

When the devcontainer is created, such as in a GitHub codespace, all the required software and packages will be installed.

Follow the [Setup Instructions in GraphAcademy](https://graphacademy.neo4j.com/courses/genai-fundamentals/4-integrating-neo4j/1-neo4j-graphrag/) to get started.

You will need to:

1. Create a new [`.env`](.env) file and copy the contents of the [`.env.example`](.env.example) file into it
2. Update the environment values in the [`.env`](.env) file with the values in the [Setup Instructions](https://graphacademy.neo4j.com/courses/genai-fundamentals/4-integrating-neo4j/1-neo4j-graphrag/)
3. Run the [`llm-knowledge-graph/test_environment.py`](./genai-fundamentals/test_environment.py) program to check the environment is set up correctly.
