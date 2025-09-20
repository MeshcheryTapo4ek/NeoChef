# NeoChef

A local recipe graph: discover meals from what you already have.

---

## 🚀 Getting Started

This guide will walk you through setting up and running the NeoChef project locally.

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) must be installed and running.
- [Python 3.12+](https://www.python.org/) is required.
- [uv](https://github.com/astral-sh/uv) is used as the package manager.

### 1. Configuration

The project uses a `.env` file for configuration, particularly for the database password.

- Copy the example file:
```bash
cp .env.example .env
```
Open the new .env file and set your desired NEO4J_PASSWORD.

###  2. Install Dependencies

Use uv to create a virtual environment and install all required packages from pyproject.toml.

  ```bash
uv sync
```

### 3. Launch the Database

The Neo4j database runs in a Docker container. Launch it from the project root:

```bash
docker-compose -f neo4j/docker-compose.yml up -d --build
```


### 4. Verify the Setup

Run the health check script to confirm that the application can connect to the database.

```bash
uv run python -m scripts.health_check
```