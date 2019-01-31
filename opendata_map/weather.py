import requests

def get_weather(api_key, location):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, api_key)
    r = requests.get(url)
    return r.json()

def get_weather_location(api_key,lattitude,longitude):
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}".format(lattitude, longitude, api_key)
    r = requests.get(url)
    return r.json()


def format_for_frontend(weather_result):

    formatted = """
    {}
    temp : {}
    """
    try:
        print(weather_result)
        weather = weather_result['weather'][0]
        forecast = "{}:{}".format(weather['main'],weather['description'])
        temperature = weather_result['main']['temp']
        formatted = formatted.format(forecast,temperature)
        print(formatted)
        return formatted.format(forecast,formatted)
    except Exception as e:
        print(e)
        return "error when loading weather data"
