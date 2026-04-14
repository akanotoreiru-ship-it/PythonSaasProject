import pandas as pd
import datetime as dt
import pickle
import os
import json
import numpy as np
from utils.get_weather import get_weather_for_24_hours
from utils.parse_isw1 import get_isw_features

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "XGB_F.pkl")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "results.json")


model = pickle.load(open(MODEL_PATH, "rb"))


model_mtime = os.path.getmtime(MODEL_PATH)
last_model_train_time = dt.datetime.utcfromtimestamp(model_mtime).strftime("%Y-%m-%dT%H:%M:%SZ")

regions = [
    "Київщина", "Харківщина", "Львівщина", "Одещина", "Донеччина",
    "Луганщина", "Херсонщина", "АР Крим", "Миколаївщина", "Чернігівщина",
    "Дніпропетровщина", "Вінниччина", "Житомирщина", "Кіровоградщина",
    "Полтавщина", "Сумщина", "Рівненщина", "Хмельниччина", "Черкащина",
    "Закарпаття", "Запоріжжя", "Івано-Франківщина"
]

region_name_map = {
    "Київщина": "Kyiv", "Харківщина": "Kharkiv", "Львівщина": "Lviv",
    "Одещина": "Odesa", "Донеччина": "Donetsk", "Луганщина": "Luhansk",
    "Херсонщина": "Kherson", "АР Крим": "Crimea", "Миколаївщина": "Mykolaiv",
    "Чернігівщина": "Chernihiv", "Дніпропетровщина": "Dnipro",
    "Вінниччина": "Vinnytsia", "Житомирщина": "Zhytomyr",
    "Кіровоградщина": "Kropyvnytskyi", "Полтавщина": "Poltava",
    "Сумщина": "Sumy", "Рівненщина": "Rivne", "Хмельниччина": "Khmelnytskyi",
    "Черкащина": "Cherkasy", "Закарпаття": "Zakarpattia",
    "Запоріжжя": "Zaporizhzhia", "Івано-Франківщина": "Ivano-Frankivsk"
}

text_df = get_isw_features()

isw_save_path = os.path.join(BASE_DIR, "data", "isw_latest_report.csv")
text_df.to_csv(isw_save_path, sep=";", index=False)
try:
    os.chmod(isw_save_path, 0o666)
except Exception:
    pass

text_df["key"] = 1

regions_forecast = {}

weather_dir = os.path.join(BASE_DIR, "data", "weather_for_24_hours")
os.makedirs(weather_dir, exist_ok=True)
try:
    os.chmod(weather_dir, 0o777)
except Exception:
    pass

for region in regions:
    print(f"Обробка {region}...")

    weather_df = get_weather_for_24_hours(region)

    if weather_df is None:
        continue

    eng_name = region_name_map.get(region, region)
    weather_path = os.path.join(weather_dir, f"weather_{eng_name}.csv")
    weather_df.to_csv(weather_path, index=False)
    
    try:
        os.chmod(weather_path, 0o666)
    except Exception:
        pass

    weather_df["region_id"] = regions.index(region)
    weather_df["key"] = 1

    df_all = weather_df.merge(text_df, on="key").drop("key", axis=1)

    feature_cols = model.get_booster().feature_names
    df_all = df_all[feature_cols]


    preds = model.predict(df_all)


    now = dt.datetime.now()
    eng_name = region_name_map.get(region, region)
    hourly = {}
    for i, pred in enumerate(preds):
        hour_time = (now + dt.timedelta(hours=i)).strftime("%H:00")
        # true = тривога очікується, false = тривоги немає
        hourly[hour_time] = bool(int(pred))

    regions_forecast[eng_name] = hourly

result = {
    "last_model_train_time": last_model_train_time,
    "last_prediction_time": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "model_name": "XGBoost (XGB_F.pkl)",
    "total_regions": len(regions_forecast),
    "regions_forecast": regions_forecast
}

def convert(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return str(o)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4, default=convert)

print(f"Прогноз збережено в {OUTPUT_PATH}")
