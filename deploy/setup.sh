#!/bin/bash
# ============================================================
# Air Alarm Prediction — EC2 Setup Script
# Run as: sudo bash setup.sh
# ============================================================
set -e

APP_DIR="/home/ubuntu/alarm-app"
VENV_DIR="$APP_DIR/venv"
SERVICE_NAME="alarm-app"

echo "========================================="
echo "  1. Updating system & installing deps"
echo "========================================="
apt-get update -y
apt-get install -y python3 python3-pip python3-venv nginx

echo "========================================="
echo "  2. Creating virtual environment"
echo "========================================="
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "========================================="
echo "  3. Installing Python packages"
echo "========================================="
pip install --upgrade pip
pip install -r "$APP_DIR/requirements.txt"

python3 -c "import nltk; nltk.download('punkt')" || true

echo "========================================="
echo "  4. Creating data directory"
echo "========================================="
mkdir -p "$APP_DIR/data"

echo "========================================="
echo "  5. Running predict.py for initial data"
echo "========================================="
cd "$APP_DIR"
"$VENV_DIR/bin/python" predict.py || echo "⚠️  predict.py failed (will retry via cron)"

echo "========================================="
echo "  6. Setting up systemd service (Gunicorn)"
echo "========================================="
cp "$APP_DIR/deploy/alarm-app.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"

echo "========================================="
echo "  7. Setting up Nginx"
echo "========================================="
rm -f /etc/nginx/sites-enabled/default
cp "$APP_DIR/deploy/nginx-alarm-app.conf" /etc/nginx/sites-available/alarm-app
ln -sf /etc/nginx/sites-available/alarm-app /etc/nginx/sites-enabled/alarm-app
nginx -t
systemctl restart nginx

echo "========================================="
echo "  8. Setting up cron (predict.py every hour)"
echo "========================================="
CRON_JOB="0 * * * * cd $APP_DIR && $VENV_DIR/bin/python predict.py >> $APP_DIR/data/predict.log 2>&1"

# Add cron job for ubuntu user (avoid duplicates)
(crontab -u ubuntu -l 2>/dev/null | grep -v "predict.py"; echo "$CRON_JOB") | crontab -u ubuntu -

echo ""
echo "========================================="
echo "  DEPLOYMENT COMPLETE!"
echo "========================================="
echo ""
echo "  Gunicorn:  sudo systemctl status $SERVICE_NAME"
echo "  Nginx:     http://<YOUR_EC2_PUBLIC_IP>"
echo "  Cron:      crontab -u ubuntu -l"
echo "  Logs:      $APP_DIR/data/predict.log"
echo ""
