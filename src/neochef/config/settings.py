import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    """
    Application settings loaded from environment variables.
    The dataclass is frozen, so the settings are immutable.
    """
    # Neo4j Database Credentials
    neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "")
    neo4j_host: str = "localhost"
    neo4j_port: int = 7687

    @property
    def neo4j_uri(self) -> str:
        """Construct the Bolt URI for the Neo4j driver."""
        return f"bolt://{self.neo4j_host}:{self.neo4j_port}"


# Create a single, immutable instance of the settings to be used across the application.
settings = Settings()