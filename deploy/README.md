# Deployment Configuration

This folder contains scripts and configurations for deploying the **Air Alarm Prediction** application to a production server (specifically tested on AWS EC2 with Ubuntu).

## Contents

- `setup.sh`: The main deployment script. It automates the entire process including dependency installation, environment setup, and service configuration.
- `alarm-app.service`: A Systemd unit file to manage the Flask application as a background service using Gunicorn.
- `nginx-alarm-app.conf`: Nginx configuration to act as a reverse proxy, serving the application on port 80 and handling static files.

## Deployment Steps

To deploy the application, follow these steps on your server:

1. **Clone the repository** to `/home/ubuntu/alarm-app`.
2. **Navigate to the deploy folder**:
   ```bash
   cd /home/ubuntu/alarm-app/deploy
   ```
3. **Execute the setup script** with sudo:
   ```bash
   sudo bash setup.sh
   ```

## What the setup script does

1. **Installs System Dependencies**: Updates the system and installs `python3`, `python3-pip`, `python3-venv`, and `nginx`.
2. **Prepares Python Environment**: Creates a virtual environment in `venv/`, upgrades pip, and installs all packages listed in `requirements.txt`.
3. **Initializes Data**: Downloads necessary NLTK data and runs `predict.py` to generate the initial forecast.
4. **Configures Systemd**: Copies `alarm-app.service` to `/etc/systemd/system/`, enables, and starts the service.
5. **Configures Nginx**: Replaces the default Nginx configuration with `nginx-alarm-app.conf`, setting up the reverse proxy and static file serving.
6. **Schedules Automation**: Adds a cron job to the `ubuntu` user to run `predict.py` every hour, ensuring forecasts are always up to date.

## Managing the Application

- **Check App Status**: `sudo systemctl status alarm-app`
- **Restart App**: `sudo systemctl restart alarm-app`
- **View Logs**:
  - Gunicorn/App logs: `journalctl -u alarm-app`
  - Prediction logs: `cat /home/ubuntu/alarm-app/data/predict.log`
  - Nginx logs: `sudo tail -f /var/log/nginx/access.log`
