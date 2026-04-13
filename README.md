# Python SaaS: Air Threat Forecasting for Ukraine

## Overview
This project is a Python-based SaaS application focusing on processing and forecasting **air alarms, explosions, and artillery fire** based on various data sources. It translates raw, open-source conflict data into actionable insight.

The goal is to predict the probability of these types of military activity using machine learning models to estimate the likelihood of upcoming security events in specific Ukrainian oblasts over defined time periods.

The system integrates information from multiple sources including:
* Intelligence reports from the Institute for the Study of War (ISW)
* Historical conflict event data
* Weather conditions
* Regional activity patterns

### Predicted Event Types
The system forecasts the probability per region of the following events:
- 🚨 **Air alarms**
- 💥 **Explosions**
- 💣 **Artillery fire**

***

## Motivation
Since the beginning of the full-scale invasion of Ukraine in 2022, open-source intelligence and data analysis have become essential tools for understanding the dynamics of the conflict. The need for fast, accessible, and data-driven situational awareness has become critical for civilians, researchers, and early responders.

This project aims to explore how machine learning and automated data processing can be applied to conflict-related data to identify patterns and estimate potential future risks. It was developed to bridge the gap between intelligence collection and actionable threat forecasting. 

***

## Project Goals
The main objectives of the project are:
* **Collect and preprocess** open-source conflict data automatically.
* **Extract useful features** from complex textual intelligence reports.
* **Analyze historical event patterns** logically across different regions.
* **Train machine learning models** to accurately forecast potential imminent threats.
* **Evaluate model performance** using standard classification and accuracy metrics.

***

## Data Sources
The project uses several layers of publicly available data to build its context:
1. **Institute for the Study of War (ISW) reports**: Used to extract structured information about military activities and developments natively.
2. **Historical event datasets**: Used to train and evaluate the predictive models with real ground-truth outcomes.
3. **Weather data**: Used as contextual features that consistently influence tactical activity patterns.

***

## Features
🔁 **Automated Data Collection:** Scheduled scripts systematically fetch and parse open intelligence sources (like ISW) and live weather feeds.

🧠 **Forecasting Models:** Employs advanced machine learning models (XGBoost) to evaluate situational arrays and predict the likelihood of future incidents.

🌍 **Regional Intelligence:** Forecasts are highly localized and processed per Ukrainian oblast, providing specific threat probabilities rather than generic national alerts.

📊 **Visualization-Ready Output:** The predictive outputs are formatted elegantly for easy integration into our Flask web dashboard and visualization panels.

🧩 **Modular Data Pipeline:** Easily extensible architecture. Extraction, merging, evaluation, and deployment scripts are strictly separated so logic modules can be added seamlessly.

☁️ **SaaS-Friendly Deployment:** Built to run on modern cloud platforms (like AWS EC2). Hosted effectively via NGINX as an environment with reliable cron job scheduling natively integrated.

***

## Project Structure
```text
├── data/                     # Raw stored datasets and parsed CSV caches
├── dataAnalysis/             # Analytical notebooks and script exploration
├── deploy/                   # Infrastructure config (nginx, systemd, setup)
├── isw_preparation/          # ISW documentation and fetching pipelines
├── models/                   # Serialized ML models ready for loading (.pkl)
├── templates/                # App HTML UI components
├── utils/                    # External APIs fetchers (Weather and ISW parsing)
├── app.py                    # Core Flask backend API to serve the web UI
├── requirements.txt          # Essential Python dependency list
└── README.md                 # You're reading it 
```

***

## Installation
Make sure you have **Python 3.8+** installed.

```bash
git clone https://github.com/akanotoreiru-ship-it/PythonSaasProject.git
cd PythonSaasProject
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

***

## Deployment Notes
This full application is deployable as a lightweight SaaS system. You can spin up the Flask frontend or inference schedulers natively, or host it robustly on cloud platforms like:

* **AWS EC2 / Lightsail** (Recommended, via robust systemd services & cron)
* Railway / Render
* Heroku

**For production environments, you may optionally:**
* Use `uWSGI` or `gunicorn` as WSGI servers.
* Add a `Dockerfile` for streamlined containerized deployment.
* Hook NGINX directly up as a reverse proxy!
