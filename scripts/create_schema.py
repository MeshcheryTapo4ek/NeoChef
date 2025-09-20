import asyncio

from neo4j import AsyncGraphDatabase

from neochef.config import logger, settings

# Define the Cypher queries for creating constraints.
# Using 'IF NOT EXISTS' makes the script idempotent (safe to run multiple times).
CREATE_RECIPE_ID_CONSTRAINT = """
CREATE CONSTRAINT recipe_id_unique IF NOT EXISTS
FOR (r:Recipe) REQUIRE r.id IS UNIQUE
"""

CREATE_INGREDIENT_NAME_CONSTRAINT = """
CREATE CONSTRAINT ingredient_name_unique IF NOT EXISTS
FOR (i:Ingredient) REQUIRE i.normalizedName IS UNIQUE
"""

async def main():
    
    """
    Connects to Neo4j and applies schema constraints.
    """
    logger.info("Connecting to Neo4j to apply schema constraints...")
    driver = None
    try:
        driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password)
        )
        
        async with driver.session() as session:
            logger.info("Applying constraint for Recipe ID...")
            await session.run(CREATE_RECIPE_ID_CONSTRAINT)
            logger.success("Constraint for Recipe ID applied.")

            logger.info("Applying constraint for Ingredient Name...")
            await session.run(CREATE_INGREDIENT_NAME_CONSTRAINT)
            logger.success("Constraint for Ingredient Name applied.")
        
        logger.info("Schema setup complete.")

    except Exception:
        logger.exception("Failed to apply schema constraints to Neo4j.")
    finally:
        if driver:
            await driver.close()


if __name__ == "__main__":
    asyncio.run(main())