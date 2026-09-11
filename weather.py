import sys
import json
import urllib.request
import urllib.parse


def geocode(city):
    url = "https://geocoding-api.open-meteo.com/v1/search?" + urllib.parse.urlencode({
        "name": city, "count": 1, "language": "ru", "format": "json"
    })
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.load(r)
    if not data.get("results"):
        return None
    return data["results"][0]


def weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode({
        "latitude": lat, "longitude": lon, "current_weather": "true"
    })
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.load(r)["current_weather"]


def main():
    city = sys.argv[1] if len(sys.argv) > 1 else "Moscow"
    place = geocode(city)
    if not place:
        print("Город не найден.")
        return
    w = weather(place["latitude"], place["longitude"])
    print(f"Погода в {place['name']}, {place.get('country', '')}:")
    print(f"  Температура: {w['temperature']}°C")
    print(f"  Ветер: {w['windspeed']} км/ч")
    print(f"  Направление: {w['winddirection']}°")


if __name__ == "__main__":
    main()