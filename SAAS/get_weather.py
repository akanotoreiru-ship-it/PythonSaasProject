import pandas as pd
import requests
import time
from datetime import datetime
import os

API_KEY = ""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGIONS_FILE = os.path.join(BASE_DIR, "regions.csv")

df_regions = pd.read_csv(REGIONS_FILE)


def get_weather_for_24_hours(region):
    try:
        city = df_regions[df_regions["region_alt"] == region]["center_city_en"].values[0]
    except:
        print(f"Region not found: {region}")
        return None

    today_date = datetime.now().strftime("%Y-%m-%d")
    location = f"{city},Ukraine"

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{today_date}/{today_date}?key={API_KEY}&include=hours"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Weather API error for {region}")
        return None

    data = response.json()
    day = data["days"][0]

    base = {
        'day_tempmax': day.get('tempmax'),
        'day_tempmin': day.get('tempmin'),
        'day_temp': day.get('temp'),
        'day_dew': day.get('dew'),
        'day_humidity': day.get('humidity'),
        'day_precip': day.get('precip'),
        'day_precipcover': day.get('precipcover'),
        'day_solarradiation': day.get('solarradiation'),
        'day_solarenergy': day.get('solarenergy'),
        'day_uvindex': day.get('uvindex'),
        'day_moonphase': day.get('moonphase'),
        'day_datetimeEpoch': int(time.mktime(datetime.strptime(day['datetime'], '%Y-%m-%d').timetuple()))
    }

    rows = []
    for hour in day["hours"][:24]:
        r = base.copy()
        r.update({
            'hour_datetimeEpoch': hour.get('datetimeEpoch'),
            'hour_temp': hour.get('feelslike'),
            'hour_humidity': hour.get('humidity'),
            'hour_dew': hour.get('dew'),
            'hour_precip': hour.get('precip'),
            'hour_precipprob': hour.get('precipprob'),
            'hour_snow': hour.get('snow'),
            'hour_snowdepth': hour.get('snowdepth'),
            'hour_windgust': hour.get('windgust'),
            'hour_windspeed': hour.get('windspeed'),
            'hour_winddir': hour.get('winddir'),
            'hour_pressure': hour.get('pressure'),
            'hour_visibility': hour.get('visibility'),
            'hour_cloudcover': hour.get('cloudcover'),
            'hour_solarradiation': hour.get('solarradiation'),
            'hour_solarenergy': hour.get('solarenergy'),
            'hour_uvindex': hour.get('uvindex')
        })
        rows.append(r)

    return pd.DataFrame(rows)


if __name__ == "__main__":
    OUTPUT_FOLDER = os.path.join(BASE_DIR, "data", "weather_for_24_hours")
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    region_map = {
        "Київщина": "kyiv",
        "Харківщина": "kharkiv",
        "Львівщина": "lviv",
        "Одещина": "odesa",
        "Донеччина": "donetsk",
        "Луганщина": "luhansk",
        "Херсонщина": "kherson",
        "АР Крим": "crimea",
        "Миколаївщина": "mykolaiv",
        "Чернігівщина": "chernihiv",
        "Дніпропетровщина": "dnipro",
        "Вінниччина": "vinnytsia",
        "Житомирщина": "zhytomyr",
        "Кіровоградщина": "kropyvnytskyi",
        "Полтавщина": "poltava",
        "Сумщина": "sumy",
        "Рівненщина": "rivne",
        "Хмельниччина": "khmelnytskyi",
        "Черкащина": "cherkasy",
        "Закарпаття": "zakarpattia",
        "Запоріжжя": "zaporizhzhia",
        "Івано-Франківщина": "ivano_frankivsk"
    }

    for region_ua, region_en in region_map.items():
        print(f"Processing {region_ua}...")

        df = get_weather_for_24_hours(region_ua)

        if df is not None and len(df) > 0:
            file_name = f"weather_{region_en}.csv"
            file_path = os.path.join(OUTPUT_FOLDER, file_name)

            df.to_csv(file_path, index=False)
            print(f"Saved: {file_path}")
        else:
            print(f"Failed for {region_ua}")
