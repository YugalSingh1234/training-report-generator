#!/bin/bash
# Server Deployment Script
# ========================
# Run this script on your server to deploy the application

set -e  # Exit on any error

echo "🚀 Starting server deployment..."

# Configuration
APP_NAME="training-report-generator"
APP_USER="appuser"
APP_DIR="/opt/$APP_NAME"
SERVICE_NAME="$APP_NAME"
DOMAIN="your-domain.com"  # Change this to your domain

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run this script as root (use sudo)"
    exit 1
fi

# Update system
print_status "Updating system packages..."
apt update && apt upgrade -y

# Install required packages
print_status "Installing required packages..."
apt install -y python3 python3-pip python3-venv nginx git supervisor curl

# Create application user
print_status "Creating application user..."
if ! id "$APP_USER" &>/dev/null; then
    useradd -r -s /bin/bash -d "$APP_DIR" "$APP_USER"
fi

# Create application directory
print_status "Setting up application directory..."
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# Clone or update repository
if [ ! -d ".git" ]; then
    print_status "Cloning repository..."
    # Replace with your actual repository URL
    git clone https://github.com/yourusername/training-report-generator.git .
else
    print_status "Updating repository..."
    git pull origin main
fi

# Create virtual environment
print_status "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
print_status "Creating application directories..."
mkdir -p logs static/uploads output
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

# Create environment file
print_status "Setting up environment configuration..."
cat > .env << EOF
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
FLASK_ENV=production
DEBUG=False
HOST=0.0.0.0
PORT=5000
UPLOAD_FOLDER=$APP_DIR/static/uploads
OUTPUT_FOLDER=$APP_DIR/output
LOG_LEVEL=INFO
LOG_FILE=$APP_DIR/logs/app.log
EOF

chown "$APP_USER:$APP_USER" .env

# Create systemd service
print_status "Creating systemd service..."
cat > "/etc/systemd/system/$SERVICE_NAME.service" << EOF
[Unit]
Description=Training Report Generator
After=network.target

[Service]
Type=exec
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 4 --timeout 120 wsgi:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
print_status "Configuring Nginx..."
cat > "/etc/nginx/sites-available/$APP_NAME" << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    location /static {
        alias $APP_DIR/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /health {
        proxy_pass http://127.0.0.1:5000/health;
        access_log off;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
EOF

# Enable Nginx site
ln -sf "/etc/nginx/sites-available/$APP_NAME" "/etc/nginx/sites-enabled/"
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

# Start and enable services
print_status "Starting services..."
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"
systemctl enable nginx
systemctl restart nginx

# Setup log rotation
print_status "Setting up log rotation..."
cat > "/etc/logrotate.d/$APP_NAME" << EOF
$APP_DIR/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $APP_USER $APP_USER
    postrotate
        systemctl reload $SERVICE_NAME
    endscript
}
EOF

# Create backup script
print_status "Creating backup script..."
cat > "$APP_DIR/backup.sh" << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/training-report-generator"
DATE=$(date +"%Y%m%d_%H%M%S")
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" -C /opt/training-report-generator \
    --exclude=venv \
    --exclude=logs \
    --exclude=static/uploads \
    --exclude=output \
    .
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete
EOF

chmod +x "$APP_DIR/backup.sh"

# Add backup to crontab
(crontab -l 2>/dev/null; echo "0 2 * * * $APP_DIR/backup.sh") | crontab -

# Setup file cleanup cron job
print_status "Setting up file cleanup automation..."
cat > "$APP_DIR/cleanup_files.sh" << 'EOF'
#!/bin/bash
# File Cleanup Script - Prevents disk space issues
OUTPUT_DIR="/opt/training-report-generator/output"
UPLOAD_DIR="/opt/training-report-generator/static/uploads"
BACKUP_DIR="/var/backups/files"
MAX_OUTPUT_FILES=50
MAX_UPLOAD_FILES=100
DAYS_TO_KEEP=30

echo "$(date): Starting file cleanup..." >> /var/log/file_cleanup.log

# Create backup of recent files
mkdir -p "$BACKUP_DIR"
find "$OUTPUT_DIR" -name "*.docx" -mtime -7 -exec cp {} "$BACKUP_DIR/" \; 2>/dev/null

# Cleanup old files
find "$OUTPUT_DIR" -name "*.docx" -mtime +$DAYS_TO_KEEP -type f -delete
find "$UPLOAD_DIR" -name "*.jpg" -mtime +$DAYS_TO_KEEP -type f -delete
find "$UPLOAD_DIR" -name "*.jpeg" -mtime +$DAYS_TO_KEEP -type f -delete
find "$UPLOAD_DIR" -name "*.png" -mtime +$DAYS_TO_KEEP -type f -delete

# Limit file count
output_count=$(find "$OUTPUT_DIR" -type f | wc -l)
if [ $output_count -gt $MAX_OUTPUT_FILES ]; then
    find "$OUTPUT_DIR" -type f -printf '%T@ %p\n' | sort -n | head -n -$MAX_OUTPUT_FILES | cut -d' ' -f2- | xargs rm -f
fi

upload_count=$(find "$UPLOAD_DIR" -type f | wc -l)
if [ $upload_count -gt $MAX_UPLOAD_FILES ]; then
    find "$UPLOAD_DIR" -type f -printf '%T@ %p\n' | sort -n | head -n -$MAX_UPLOAD_FILES | cut -d' ' -f2- | xargs rm -f
fi

echo "$(date): File cleanup completed. Output: $output_count files, Upload: $upload_count files" >> /var/log/file_cleanup.log
EOF

chmod +x "$APP_DIR/cleanup_files.sh"

# Add file cleanup to crontab (runs daily at 3 AM)
(crontab -l 2>/dev/null; echo "0 3 * * * $APP_DIR/cleanup_files.sh") | crontab -

# Setup file monitoring
print_status "Installing file monitoring..."
cp file_monitor.py "$APP_DIR/"
chown "$APP_USER:$APP_USER" "$APP_DIR/file_monitor.py"

# Add file monitoring to crontab (runs every 6 hours)
(crontab -l 2>/dev/null; echo "0 */6 * * * cd $APP_DIR && python3 file_monitor.py >> /var/log/file_monitor.log 2>&1") | crontab -

# Setup firewall (if ufw is available)
if command -v ufw &> /dev/null; then
    print_status "Configuring firewall..."
    ufw allow ssh
    ufw allow 'Nginx Full'
    ufw --force enable
fi

# SSL Certificate (Let's Encrypt)
print_status "Setting up SSL certificate..."
if command -v certbot &> /dev/null; then
    certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --non-interactive --agree-tos --email admin@"$DOMAIN"
else
    print_warning "Certbot not installed. Install it manually for SSL: sudo apt install certbot python3-certbot-nginx"
fi

# Final status check
print_status "Checking service status..."
systemctl status "$SERVICE_NAME" --no-pager
systemctl status nginx --no-pager

print_status "Testing application..."
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    print_status "Application is running successfully!"
else
    print_warning "Application health check failed. Check logs: journalctl -u $SERVICE_NAME"
fi

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "📊 Next steps:"
echo "1. Update DNS to point to this server's IP"
echo "2. Test your application at: http://$DOMAIN"
echo "3. Monitor logs: journalctl -u $SERVICE_NAME -f"
echo "4. Check application health: curl http://$DOMAIN/health"
echo ""
echo "📁 Important paths:"
echo "   Application: $APP_DIR"
echo "   Logs: $APP_DIR/logs/"
echo "   Service: systemctl status $SERVICE_NAME"
echo "   Nginx: systemctl status nginx"
echo ""
echo "🔧 Management commands:"
echo "   Restart app: systemctl restart $SERVICE_NAME"
echo "   View logs: journalctl -u $SERVICE_NAME -f"
echo "   Backup: $APP_DIR/backup.sh"
EOF
