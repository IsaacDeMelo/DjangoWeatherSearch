from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Aqui carregamos seu HTML principal

def projetos(request):
    return render(request, 'projetos.html')

def contato(request):
    return render(request, 'contato.html')

import requests
import pycountry  # Biblioteca para converter códigos de países
from .translations import COUNTRY_TRANSLATIONS

def get_country_name(country_code):
    """Converte código de país (ex: 'NP') para nome completo (ex: 'Nepal')"""
    country = pycountry.countries.get(alpha_2=country_code)
    if country:
        return COUNTRY_TRANSLATIONS.get(country.name, country.name)  # Usa a tradução se existir
    return country.name if country else country_code

def weather_view(request):
    api_key = "2e41e28f11931e8b0af4db4d0bb890e7"  
    city = request.GET.get("city", "São Paulo")  
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt"

    response = requests.get(url)
    weather_data = response.json()

    print(weather_data)  # Isso ajudará a ver os dados no terminal

    if response.status_code == 200:
        country_code = weather_data["sys"]["country"]  # Código do país (ex: 'NP')
        country_name = get_country_name(country_code)  # Converte para nome completo

        clima = {
            "cidade": weather_data["name"],
            "pais": country_name,
            "temperatura": weather_data["main"]["temp"],
            "temperatura_minima": weather_data["main"]["temp_min"],
            "temperatura_maxima": weather_data["main"]["temp_max"],
            "descricao": weather_data["weather"][0]["description"].capitalize(),
            "icone": weather_data["weather"][0]["icon"]
            
        }
    else:
        clima = None

    return render(request, "weather.html", {"clima": clima, "cidade": city})
