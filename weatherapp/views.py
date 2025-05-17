from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
from decouple import config

# Create your views here.
def home(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'

    OPENWEATHER_API_KEY = config('OPENWEATHER_API_KEY')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}'
    PARAMS = {'units':'metric'}


    try:
        weather_data = requests.get(url, params=PARAMS).json()

        # Raise an exception if city is not found (code 404)
        if weather_data.get('cod') != 200:
            raise ValueError("Invalid city name")

        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        # Only run Google search if city is valid
        GOOGLE_API_KEY = config('GOOGLE_API_KEY')
        GOOGLE_SEARCH_ENGINE_ID = config('GOOGLE_SEARCH_ENGINE_ID')
        query = f"{city} city skyline wallpaper"
        page = 1
        start = (page - 1) * 10 + 1
        searchType = 'image'
        city_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

        data = requests.get(city_url).json()
        count = 1
        search_items = data.get("items")
        image_url = search_items[1]['link']

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occured': False,
            'image_url': image_url
        })
    except:
        exception_occured = True
        messages.error(request, 'entered data si not available to API')
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {'description': 'clear sky', 'icon':'01d', 'temp':'25', 'day':day, 'city':'indore', 'exception_occured':True})
    
