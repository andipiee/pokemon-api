# Pokemon API

A FastAPI-based REST API that scrapes Pokemon data and provides it through JSON:API compliant endpoints.

## Features

- Scrapes Pokemon data from PokeAPI (first 151 Pokemon only) -> can be configured later
- Stores data in SQLite database
- Provides REST API endpoints following JSON:API specification
- Supports pagination and type filtering
- Async database operations for better performance
- On-runtime data scraping and database population

## Tech Stack

- Python 3.11
- FastAPI (running on Uvicorn)
- aiosqlite

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/andipiee/pokemon-api.git
cd pokemon-api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```
The API will be available at http://localhost:8000

Note: On first run, the application will scrape data for the original 151 Pokemon from PokeAPI and populate the database. This may take a few minutes.

## API Endpoints

### List Pokemon
```
GET /api/pokemon
```
Query Parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10)
- `type_filter`: Filter by Pokemon type

### Get Single Pokemon
```
GET /api/pokemon/{id}
```

## Project Structure

```
pokemon-api/
├── main.py             # Main application file
├── requirements.txt    # Python dependencies
├── db_setup.py        # DB setup initation and repo function
├── pokemon_class.py   # Pokemon Base Model
├── scrapper.py        # Pokemon scrapper
├── server.py          # Fast API server setup
├── Dockerfile         # Docker container definition
├── docker-compose.yml # Docker services configuration
└── README.md          # Project documentation
```

## Database

The application uses SQLite for data storage.

Database schema:
```sql
CREATE TABLE pokemon (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    height REAL,
    weight REAL,
    types TEXT,
    base_experience INTEGER,
    sprite_url TEXT
)
```

## API Documentation

After starting the application, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Response Format

The API follows JSON:API specification. Example response:

```json
{
  "data": [
    {
      "type": "pokemon",
      "id": "1",
      "attributes": {
        "name": "bulbasaur",
        "height": 0.7,
        "weight": 6.9,
        "types": ["grass", "poison"],
        "base_experience": 64,
        "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"
      }
    }
  ]
}
```

## Testing

You can test the API using the Swagger UI or with curl:

```bash
# List Pokemon
curl http://localhost:8000/api/pokemon

# Get specific Pokemon
curl http://localhost:8000/api/pokemon/1

# Filter by type
curl http://localhost:8000/api/pokemon?type_filter=grass

# Pagination
curl http://localhost:8000/api/pokemon?page=2&page_size=20
```

## Data Modeling Assumptions

### Base Model Design

The application uses Pydantic models to define the structure and validation of Pokemon data. The design is based on several key assumptions:

#### 1. Data Attributes
We assume each Pokemon has the following core attributes:
- `id`: Unique identifier (1-151 only)
- `name`: Pokemon name
- `height`: Physical height in meters
- `weight`: Physical weight in kilograms
- `types`: List of Pokemon types
- `base_experience`: Starting experience points
- `sprite_url`: URL to the Pokemon's front default sprite

#### 2. JSON:API Specification Compliance
The response model follows JSON:API specification with a structured format:
```json
{
  "data": [
    {
      "type": "pokemon",
      "id": "string",
      "attributes": {
        // Detailed Pokemon attributes
      }
    }
  ]
}
```

#### 3. Data Transformations
Several data transformations are applied during scraping:
- Height is converted from decimeters to meters (divided by 10)
- Weight is converted from hectograms to kilograms (divided by 10)
- Pokemon types are stored as a list
- Sprite URLs are using the front default sprite

#### 4. Error Handling Assumptions
- Missing `base_experience` defaults to 0
- Pokemon without a sprite will have a null/empty URL
- Type information is extracted from the first available type

#### 5. Scraping Assumptions
- The scraper runs on application startup
- Only the original 151 Pokemon (Generation 1) are scraped
- Data is fetched from PokeAPI and stored locally
- The scraping process is performed once per application startup
- If the database already contains data, the scraper will skip the Pokemon

## Example of Full Data Model

```python
class PokemonAttributes(BaseModel):
    name: str               # Pokemon name
    height: float           # Height in meters
    weight: float           # Weight in kilograms
    types: List[str]        # Pokemon types
    base_experience: int    # Starting XP
    sprite_url: str         # Default sprite URL

class PokemonData(BaseModel):
    type: str = "pokemon"   # JSON:API type
    id: str                 # Unique identifier
    attributes: PokemonAttributes  # Detailed attributes
```