import asyncio
import logging
from db_setup import DatabaseManager
from scrapper import PokemonScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def main():
    # Initialize database manager
    db_manager = DatabaseManager()

    # Initialize the database
    await db_manager.init_db()

    # Create scraper instance
    pokemon_scraper = PokemonScraper(db_manager)

    # Run the scraper to populate the database
    # Get first generation pokemon (151)
    await pokemon_scraper.scrape_pokemon(151)


if __name__ == "__main__":
    asyncio.run(main())