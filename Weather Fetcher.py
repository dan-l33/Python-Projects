import requests
import config

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q="
city = input("Enter a city name: ")
request_url = BASE_URL + city + "&appid=" + config.API_KEY
response = requests.get(request_url)

if response.status_code == 200:
    data = response.json()
    weather = data["weather"][0]["description"]
    print("Weather: ", weather)
    temperature = round(data["main"]["temp"]-273.15, 1)
    print("Temperture: ", temperature, "°C")
else:
    print("Error encountered")