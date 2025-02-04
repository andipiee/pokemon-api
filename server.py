import logging
import json
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from db_setup import DatabaseManager
from pokemon_class import PokemonResponse, PokemonData, PokemonAttributes
from scrapper import PokemonScraper

logger = logging.getLogger(__name__)


class PokemonServer:
    def __init__(self, db_manager: DatabaseManager, pokemon_scraper: PokemonScraper):
        self.app = FastAPI(title="Pokemon API")
        self.db_manager = db_manager
        self.pokemon_scraper = pokemon_scraper

        # Setup routes
        self.setup_routes()

    def setup_routes(self):
        @self.app.on_event("startup")
        async def startup_event():
            await self.db_manager.init_db()
            await self.pokemon_scraper.scrape_pokemon(151) # remove this parameter to scrape all pokemon data

        @self.app.get("/api/pokemon", response_model=PokemonResponse)
        async def get_pokemon(
                page: int = Query(1, ge=1),
                page_size: int = Query(10, ge=1, le=100),
                type_filter: Optional[str] = None
        ):
            try:
                pokemon_list = await self.db_manager.get_pokemon(
                    page=page,
                    page_size=page_size,
                    type_filter=type_filter
                )

                if not pokemon_list:
                    raise HTTPException(status_code=404, detail="No Pokemon found")

                # Convert to PokemonData format
                response_data = []
                for pokemon in pokemon_list:
                    pokemon_data = PokemonData(
                        type="pokemon",
                        id=str(pokemon['id']),
                        attributes=PokemonAttributes(
                            name=pokemon['name'],
                            height=pokemon['height'],
                            weight=pokemon['weight'],
                            types=json.loads(pokemon['types']),
                            base_experience=pokemon['base_experience'],
                            sprite_url=pokemon['sprite_url']
                        )
                    )
                    response_data.append(pokemon_data)

                return PokemonResponse(data=response_data)

            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error fetching Pokemon: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")

        @self.app.get("/api/pokemon/{pokemon_id}", response_model=PokemonData)
        async def get_pokemon_by_id(
                pokemon_id: int
        ):
            try:
                logger.info(f"Received request for Pokemon ID: {pokemon_id}")
                pokemon = await self.db_manager.get_pokemon_by_id(pokemon_id=pokemon_id)

                if not pokemon:
                    raise HTTPException(status_code=404, detail="Pokemon not found")

                return PokemonData(
                    type="pokemon",
                    id=str(pokemon['id']),
                    attributes=PokemonAttributes(
                        name=pokemon['name'],
                        height=pokemon['height'],
                        weight=pokemon['weight'],
                        types=json.loads(pokemon['types']),
                        base_experience=pokemon['base_experience'],
                        sprite_url=pokemon['sprite_url']
                    )
                )

            except HTTPException:
                raise
            except Exception as e:
                logger.warning(f"Error fetching Pokemon {pokemon_id}: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")