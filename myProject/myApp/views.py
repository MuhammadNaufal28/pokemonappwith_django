import random
import requests
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from googletrans import Translator


#function for translate text
def translate_text(text, dest_language='en'):
    translator = Translator()
    translated = translator.translate(text, dest=dest_language)
    return translated.text

#function for ability detail
def ability_detail(request, ability_name):
    response = requests.get(f'{BASE_API_URL}/ability/{ability_name}')
    if response.status_code == 200:
        ability_data = response.json()
        effect = ability_data['effect_entries'][0]['effect']
        return JsonResponse({'effect': effect})
    else:
        return JsonResponse({'error': 'Ability not found'}, status=404)

#function for translate ability effect
def translate_ability_effect(request, ability_name):
    response = requests.get(f'{BASE_API_URL}/ability/{ability_name}')
    if response.status_code == 200:
        ability_data = response.json()
        effect = ability_data['effect_entries'][0]['effect']
        translated_effect = translate_text(effect)
        return JsonResponse({'effect': effect, 'translated_effect': translated_effect})
    else:
        return JsonResponse({'error': 'Ability not found'}, status=404)

#function for home and get the api
def home(request):
    pokemon_data = None
    if 'pokemon_name' in request.GET:
        pokemon_name = request.GET['pokemon_name']
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}')
        if response.status_code == 200:
            pokemon_data = response.json()
    
    return render(request, 'myApp/home.html', {'pokemon_data': pokemon_data})
#url from the api
BASE_API_URL = 'https://pokeapi.co/api/v2'

#
def gatcha_result(request):
    # Implement this view if you have specific logic for results
    return render(request, 'myApp/gatcha.html')


# Halaman untuk mencari Pokemon
def pokemon_search(request):
    if request.method == 'GET' and 'name' in request.GET:
        name = request.GET['name'].lower()
        response = requests.get(f'{BASE_API_URL}/pokemon/{name}')
        if response.status_code == 200:
            pokemon_data = response.json()
            return render(request, 'pokemon_detail.html', {'pokemon': pokemon_data})
        else:
            return render(request, 'home.html', {'error': 'Pokemon not found'})
    return render(request, 'pokemon_search.html')

def pokemon_detail(request, name):
    response = requests.get(f'{BASE_API_URL}/pokemon/{name}')
    if response.status_code == 200:
        pokemon_data = response.json()
        return render(request, 'pokemon_detail.html', {'pokemon': pokemon_data})
    else:
        return render(request, 'error.html', {'error': 'Pokemon not found'})

# Halaman untuk menampilkan efek dari ability
def ability_detail(request, ability_name):
    response = requests.get(f'{BASE_API_URL}/ability/{ability_name}')
    if response.status_code == 200:
        ability_data = response.json()
        effect = ability_data['effect_entries'][0]['effect']
        return JsonResponse({'effect': effect})
    else:
        return JsonResponse({'error': 'Ability not found'}, status=404)

#fungsi gacha
def gatcha(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        gender = random.choices(['male', 'female'], [0.5, 0.5])[0]
        now = datetime.now()
        time_of_day = 'day' if now.hour >= 6 and now.hour < 18 else 'night'
        
        pokemons = {
            'forest': ['bulbasaur', 'ivysaur', 'venusaur'],
            'cave': ['geodude', 'gravelar', 'golem'],
            'mountain': ['machop', 'machoke', 'machamp'],
            'sea': ['squirtle', 'wartortle', 'blastoise']
        }
        
        pokemon_names = pokemons.get(location, [])
        if pokemon_names:
            selected_pokemon = random.choice(pokemon_names)
            pokemon_data = requests.get(f'https://pokeapi.co/api/v2/pokemon/{selected_pokemon}').json()
            gatcha_result = {
                'name': pokemon_data['name'],
                'sprites': pokemon_data['sprites'],
                'height': pokemon_data['height'],
                'weight': pokemon_data['weight'],
                'base_experience': pokemon_data['base_experience'],
                'location': location,
                'gender': gender
            }
        else:
            gatcha_result = None
        
        return render(request, 'myApp/gatcha.html', {'gatcha_result': gatcha_result})
    
    return render(request, 'myApp/gatcha.html')

# def gatcha(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        time_of_day = 'day' if datetime.datetime.now().hour < 18 else 'night'
        gender_multiplier = 1.5

        # Daftar Pokémon untuk lokasi dan encounter conditions
        pokemon_data = {
            'forest': ['bulbasaur', 'charmander', 'squirtle'],
            'cave': ['zubat', 'geodude', 'onix'],
            'mountain': ['machop', 'geodude', 'ponyta'],
            'sea': ['psyduck', 'tentacool', 'shellder']
        }

        # Filter Pokémon berdasarkan lokasi
        pokemons = pokemon_data.get(location, [])

        if pokemons:
            selected_pokemon = random.choice(pokemons)
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{selected_pokemon}')
            if response.status_code == 200:
                gatcha_result = response.json()

                # Simulasi gender multiplier (contoh)
                gender_chance = random.random()
                if gender_chance < 0.5:  # 50% chance to get female Pokémon
                    gatcha_result['gender'] = 'Female'
                else:
                    gatcha_result['gender'] = 'Male'
                
                gatcha_result['location'] = location
                return render(request, 'gatcha_result.html', {'gatcha_result': gatcha_result})
    
    return render(request, 'gatcha.html')