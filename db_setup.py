import aiosqlite
import logging
import json

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, db_path='pokemon.db'):
        self.db_path = db_path

    async def init_db(self):
        """Initialize the database with pokemon table"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS pokemon (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    height REAL,
                    weight REAL,
                    types TEXT,
                    base_experience INTEGER,
                    sprite_url TEXT
                )
            ''')
            await db.commit()
        logger.info("Database initialized")

    async def insert_pokemon(self, pokemon_data):
        """Insert a single Pokemon into the database"""
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    INSERT OR REPLACE INTO pokemon 
                    (id, name, height, weight, types, base_experience, sprite_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    pokemon_data["id"],
                    pokemon_data["name"],
                    pokemon_data["height"],
                    pokemon_data["weight"],
                    json.dumps(pokemon_data["types"]),
                    pokemon_data["base_experience"],
                    pokemon_data["sprite_url"]
                ))
                await db.commit()
                logger.info(f"Added Pokemon: {pokemon_data['name']}")
            except Exception as e:
                logger.error(f"Error inserting Pokemon {pokemon_data['name']}: {e}")
                await db.rollback()

    async def get_pokemon(self, page=1, page_size=10, type_filter=None):
        """Retrieve Pokemon with optional filtering and pagination"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            query = "SELECT * FROM pokemon"
            params = []

            if type_filter:
                query += " WHERE types LIKE ?"
                params.append(f"%{type_filter}%")

            query += " LIMIT ? OFFSET ?"
            params.extend([page_size, (page - 1) * page_size])

            cursor = await db.execute(query, params)
            pokemon_list = await cursor.fetchall()

            return [dict(pokemon) for pokemon in pokemon_list]