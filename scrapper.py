import requests
import asyncio
import logging
from db_setup import DatabaseManager

logger = logging.getLogger(__name__)


class PokemonScraper:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    async def scrape_pokemon(self, total_pokemon: int = None):
        """Scrape Pokemon data from PokeAPI"""
        try:
            # Get total number of Pokemon if not specified
            if total_pokemon is None:
                response = requests.get("https://pokeapi.co/api/v2/pokemon/")
                if response.status_code != 200:
                    raise Exception("Failed to fetch Pokemon count")
                total_pokemon = response.json()['count']

            logger.info(f"Found {total_pokemon} Pokemon to scrape")

            # Scrape all Pokemon
            for pokemon_id in range(1, total_pokemon + 1):
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")

                # Check if database has data
                existing_pokemon = await self.db_manager.get_pokemon(page_size=1)
                if existing_pokemon:
                    logger.info(f"Pokemon with id {pokemon_id} already exists in database")
                    continue

                # Rate limiting
                await asyncio.sleep(0.5)  # 500ms delay between requests

                if response.status_code == 200:
                    data = response.json()

                    # Prepare Pokemon data
                    pokemon_data = {
                        "id": pokemon_id,
                        "name": data['name'],
                        "height": data['height'] / 10,  # Convert to meters
                        "weight": data['weight'] / 10,  # Convert to kilograms
                        "types": [t['type']['name'] for t in data['types']],
                        "base_experience": data.get('base_experience', 0),
                        "sprite_url": data['sprites']['front_default']
                    }

                    # Insert into database
                    await self.db_manager.insert_pokemon(pokemon_data)

                    logger.info(f"Added Pokemon {pokemon_id}/{total_pokemon}: {pokemon_data['name']}")
                else:
                    logger.error(f"Failed to fetch Pokemon {pokemon_id}/{total_pokemon}")

        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            raise
