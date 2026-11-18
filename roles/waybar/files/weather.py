#!/usr/bin/env python

import json
import requests
from datetime import datetime

# Fallback-Icon für unbekannte Wetter-Codes
DEFAULT_ICON = '🌈'

WEATHER_CODES = {
    '113': '☀️',
    '116': '⛅️',
    '119': '☁️',
    '122': '☁️',
    '143': '🌫',
    '149': '🌦', # Nieselregen (der gefehlt hat)
    '176': '🌦',
    '179': '🌧',
    '182': '🌧',
    '185': '🌧',
    '200': '⛈',
    '227': '🌨',
    '230': '❄️',
    '248': '🌫',
    '260': '🌫',
    '263': '🌦',
    '266': '🌦',
    '281': '🌧',
    '284': '🌧',
    '293': '🌦',
    '296': '🌦',
    '299': '🌧',
    '302': '🌧',
    '305': '🌧',
    '308': '🌧',
    '311': '🌧',
    '314': '🌧',
    '317': '🌧',
    '320': '🌨',
    '323': '🌨',
    '326': '🌨',
    '329': '❄️',
    '332': '❄️',
    '335': '❄️',
    '338': '❄️',
    '350': '🌧',
    '353': '🌦',
    '356': '🌧',
    '359': '🌧',
    '362': '🌧',
    '365': '🌧',
    '368': '🌨',
    '371': '❄️',
    '374': '🌧',
    '377': '🌧',
    '386': '⛈',
    '389': '🌩',
    '392': '⛈',
    '395': '❄️'
}

data = {}

def get_weather():
    try:
        # timeout=10 verhindert, dass das Skript ewig hängt
        response = requests.get("https://wttr.in/04808?format=j1", timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, Exception):
        # Falls offline (z.B. nach Suspend), geben wir eine saubere Fehlermeldung an Waybar aus
        return None

weather = get_weather()

if not weather:
    # Saubere Fallback-Ausgabe für Waybar bei Verbindungsproblemen
    data['text'] = "󰤮 Offline"
    data['tooltip'] = "Keine Verbindung zu wttr.in (WLAN rekonnektiert?)"
    print(json.dumps(data))
    exit(0)

def format_time(time):
    return time.replace("00", "").zfill(2)

def format_temp(temp):
    return (temp + "°").ljust(3)

def format_chances(hour):
    chances = {
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind"
    }

    conditions = []
    for event in chances.keys():
        if int(hour.get(event, 0)) > 0:
            conditions.append(chances[event] + " " + hour[event] + "%")
    return ", ".join(conditions)

# .get(code, DEFAULT_ICON) verhindert das Abstürzen bei unbekannten Codes!
current_code = weather['current_condition'][0]['weatherCode']
current_icon = WEATHER_CODES.get(current_code, DEFAULT_ICON)

data['text'] = f"{current_icon} {weather['current_condition'][0]['FeelsLikeC']}°C"

data['tooltip'] = f"<b>{weather['current_condition'][0]['weatherDesc'][0]['value']} {weather['current_condition'][0]['temp_C']}°C</b>\n"
data['tooltip'] += f"Feels like: {weather['current_condition'][0]['FeelsLikeC']}°C\n"
data['tooltip'] += f"Wind: {weather['current_condition'][0]['windspeedKmph']}Km/h\n"
data['tooltip'] += f"Humidity: {weather['current_condition'][0]['humidity']}%\n"

for i, day in enumerate(weather['weather']):
    data['tooltip'] += f"\n<b>"
    if i == 0:
        data['tooltip'] += "Today, "
    if i == 1:
        data['tooltip'] += "Tomorrow, "
    data['tooltip'] += f"{day['date']}</b>\n"
    data['tooltip'] += f"⬆️ {day['maxtempC']}° ⬇️ {day['mintempC']}° "
    data['tooltip'] += f"🌅 {day['astronomy'][0]['sunrise']} 🌇 {day['astronomy'][0]['sunset']}\n"
    
    for hour in day['hourly']:
        if i == 0:
            if int(format_time(hour['time'])) < datetime.now().hour - 2:
                continue
        hour_code = hour['weatherCode']
        hour_icon = WEATHER_CODES.get(hour_code, DEFAULT_ICON)
        
        data['tooltip'] += f"{format_time(hour['time'])} {hour_icon} {format_temp(hour['FeelsLikeC'])} {hour['weatherDesc'][0]['value']}, {format_chances(hour)}\n"

print(json.dumps(data))