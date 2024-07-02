from django.shortcuts import render
import requests

def pokemon_list(request):
    name = request.GET.get('name')
    type = request.GET.get('type')
    URL = "https://pokeapi.co/api/v2/pokemon?limit=100"
    response = requests.get(URL)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching data from PokeAPI")

    all_pokemons = response.json().get('results', [])

    filtered_pokemons = []

    for pokemon in all_pokemons:
        pokemon_data = requests.get(pokemon["url"]).json()
        if name and name.lower() not in pokemon_data["name"].lower():
            continue
        types = [t["type"]["name"] for t in pokemon_data["types"]]
        if type and type.lower() not in types:
            continue
        filtered_pokemons.append({
            "name": pokemon_data["name"],
            "image": pokemon_data["sprites"]["front_default"],
            "type": ", ".join(types)
        })

    context = {'pokemons': filtered_pokemons}
    return render(request, 'pokemons/index.html', context)

