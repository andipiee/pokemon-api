import uvicorn
import logging
from db_setup import DatabaseManager
from scrapper import PokemonScraper
from server import PokemonServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    # Initialize components
    db_manager = DatabaseManager()
    pokemon_scraper = PokemonScraper(db_manager)
    server = PokemonServer(db_manager, pokemon_scraper)

    # Run the server
    uvicorn.run(server.app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()