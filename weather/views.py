import requests
from datetime import datetime, timedelta
from django.shortcuts import render
from .models import WeatherRecord

API_KEY = "9a523a7822bd1ae4fd4d6af6b8e2b787"


def get_weather(city):
    """
    Fetch current weather data for a city from OpenWeatherMap.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return None

    return {
        "city": response["name"],
        "temperature": response["main"]["temp"],
        "description": response["weather"][0]["description"],
    }

def current_location(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    weather = None

    if lat and lon:
        api_key = "9a523a7822bd1ae4fd4d6af6b8e2b787"  
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url).json()

        if response.get("cod") == 200:
            weather = {
                "city": response.get("name"),
                "temperature": response["main"]["temp"],
                "description": response["weather"][0]["description"],
            }
        else:
            print("API Error:", response)

    return render(request, "weather/current.html", {"weather": weather})


def home(request):
    """
    Show current weather for a city and optionally the weather history (last 3 days).
    """
    city = request.GET.get("city")
    show_history = request.GET.get("show_history")
    context = {}

    if city:
        weather = get_weather(city)

        if weather:
            WeatherRecord.objects.create(
                city=weather["city"],
                temperature=weather["temperature"],
                description=weather["description"]
            )
            context["weather"] = weather

            if show_history == "1":
                three_days_ago = datetime.now() - timedelta(days=3)
                history = WeatherRecord.objects.filter(
                    city__iexact=city,
                    date__gte=three_days_ago
                ).order_by("-date")[:3]

                context["history"] = history

    return render(request, "weather/home.html", context)


def compare(request):
    
    city1 = request.GET.get("city1")
    city2 = request.GET.get("city2")
    context = {}

    if city1 and city2:
        weather1 = get_weather(city1)
        weather2 = get_weather(city2)

        context["weather1"] = weather1
        context["weather2"] = weather2

    return render(request, "weather/compare.html", context)
