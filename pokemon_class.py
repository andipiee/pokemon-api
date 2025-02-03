from pydantic import BaseModel
from typing import List


class PokemonAttributes(BaseModel):
    name: str
    height: float
    weight: float
    types: List[str]
    base_experience: int
    sprite_url: str


class PokemonData(BaseModel):
    type: str = "pokemon"
    id: str
    attributes: PokemonAttributes


class PokemonResponse(BaseModel):
    data: List[PokemonData]