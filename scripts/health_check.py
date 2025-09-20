import asyncio

from neo4j import AsyncGraphDatabase

# Импортируем наши централизованные настройки и логгер
from neochef.config import logger, settings


async def main():
    """
    Establishes a connection to the Neo4j database and verifies connectivity.
    """
    logger.info(f"Attempting to connect to Neo4j at {settings.neo4j_uri}...")

    # Используем асинхронный драйвер
    driver = None
    try:
        # Подключаемся, используя URI и учетные данные из нашего settings-объекта
        driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password)
        )
        
        # verify_connectivity() - это встроенный в драйвер "пинг", 
        # который проверяет, что база жива и доступна.
        await driver.verify_connectivity()

        # Используем специальный метод .success() от loguru для красивого вывода
        logger.success("Connection to Neo4j established successfully!")

    except Exception as e:
        # .exception() автоматически запишет в лог полный traceback ошибки
        logger.exception(
            "Failed to connect to Neo4j. Please check your settings and ensure "
            "the Docker container is running."
        )
    finally:
        if driver:
            await driver.close()


if __name__ == "__main__":
    asyncio.run(main())