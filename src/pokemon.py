import requests
import json

BASE_URL = "https://pokeapi.co/api/v2"


def get_pokemon(pokemon_id=35):
    url = f"{BASE_URL}/pokemon/{pokemon_id}"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    pokemon_dict = json.loads(response.text)
    pokemon = {
        "name": pokemon_dict.get("name"),
        "ability": pokemon_dict.get("abilities")[0].get("ability").get("name"),
    }

    return pokemon
