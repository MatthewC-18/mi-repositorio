import requests
import os
import csv
from datetime import datetime

# Coordenadas de Madrid
MADRID_LAT = 40.4168  # Latitud de Madrid
MADRID_LONGITUDE = -3.7038  # Longitud de Madrid
API_KEY = "dd272e4e6c6073d32fc685ff8dc91569"
FILE_NAME = "/home/lorenalopez/CityWeather/clima-madrid-hoy.csv"

def get_weather(lat, lon, api):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"cod": response.status_code}

def process(json):
    normalized_dict = {
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Temperatura": json["main"]["temp"],
        "Humedad": json["main"]["humidity"],
        "Presión": json["main"]["pressure"],
        "Velocidad del viento": json["wind"]["speed"],
        "dt": json.get("dt", "N/A"),
        "coord_lon": json["coord"].get("lon", "N/A"),
        "coord_lat": json["coord"].get("lat", "N/A"),
        "weather_0_id": json["weather"][0].get("id", "N/A"),
        "weather_0_main": json["weather"][0].get("main", "N/A"),
        "weather_0_description": json["weather"][0].get("description", "N/A"),
        "weather_0_icon": json["weather"][0].get("icon", "N/A"),
        "base": json.get("base", "N/A"),
        "main_temp": json["main"].get("temp", "N/A"),
        "main_feels_like": json["main"].get("feels_like", "N/A"),
        "visibility": json.get("visibility", "N/A"),
        "wind_speed": json["wind"].get("speed", "N/A"),
        "wind_deg": json["wind"].get("deg", "N/A"),
        "clouds_all": json.get("clouds", {}).get("all", "N/A"),
        "sys_type": json.get("sys", {}).get("type", "N/A"),
        "sys_id": json.get("sys", {}).get("id", "N/A"),
        "sys_country": json.get("sys", {}).get("country", "N/A"),
        "sys_sunrise": json.get("sys", {}).get("sunrise", "N/A"),
        "sys_sunset": json.get("sys", {}).get("sunset", "N/A"),
        "timezone": json.get("timezone", "N/A"),
        "id": json.get("id", "N/A"),
        "name": json.get("name", "N/A"),
        "cod": json.get("cod", "N/A"),
    }
    return normalized_dict

def write2csv(json_response, csv_filename):
    fieldnames = [
        "Fecha", "Temperatura", "Humedad", "Presión", "Velocidad del viento",
        "dt", "coord_lon", "coord_lat", "weather_0_id", "weather_0_main",
        "weather_0_description", "weather_0_icon", "base", "main_temp",
        "main_feels_like", "visibility", "wind_speed", "wind_deg",
        "clouds_all", "sys_type", "sys_id", "sys_country", "sys_sunrise",
        "sys_sunset", "timezone", "id", "name", "cod"
    ]
    
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        
        writer.writerow(json_response)

def main():
    print("===== Bienvenido a Madrid-Clima =====")
    madrid_weather = get_weather(lat=MADRID_LAT, lon=MADRID_LONGITUDE, api=API_KEY)
    
    if madrid_weather['cod'] != 404:
        processed_weather = process(madrid_weather)
        write2csv(processed_weather, FILE_NAME)
        print("Datos climatológicos guardados correctamente en", FILE_NAME)
    else:
        print("Ciudad no disponible o API KEY no válida")

if __name__ == '__main__':
    main()
