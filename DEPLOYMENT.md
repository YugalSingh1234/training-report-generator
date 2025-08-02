# Training Report Generator - Production Deployment Guide

## 🏭 Industry-Level Deployment

This document outlines the complete process for deploying the Training Report Generator at an industry level.

## 📋 Prerequisites

- Python 3.11+
- Docker (optional)
- Redis (for caching and queuing)
- Nginx (for reverse proxy)
- SSL Certificate
- Domain name

## 🚀 Quick Start

### Local Development
```bash
# Clone repository
git clone <your-repo-url>
cd Word_Generator_Project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run application
python app_clean.py
```

### Production Deployment

#### Option 1: Docker Deployment
```bash
# Build image
docker build -t training-report-generator .

# Run container
docker run -d \
  --name training-app \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -v $(pwd)/logs:/app/logs \
  training-report-generator
```

#### Option 2: Server Deployment
```bash
# On your server
chmod +x deploy.sh
./deploy.sh
```

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
- `FLASK_ENV`: Set to `production`
- `DATABASE_URL`: Database connection string (if needed)
- `UPLOAD_FOLDER`: Path for file uploads
- `OUTPUT_FOLDER`: Path for generated documents

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /path/to/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 📊 Monitoring

### Health Checks
- `GET /health` - Application health status
- `GET /metrics` - System metrics

### Logging
- Application logs: `logs/app.log`
- Access logs: `logs/access.log`
- Error logs: `logs/error.log`

## 🔒 Security Features

- File upload validation
- MIME type checking
- Rate limiting
- Secure secret key generation
- Input sanitization
- Error handling

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=.

# Security scan
bandit -r .
```

## 📈 Performance Optimization

- Use Gunicorn with multiple workers
- Enable gzip compression in Nginx
- Implement Redis caching
- Use CDN for static files
- Optimize Docker image layers

## 🚨 Troubleshooting

### Common Issues

1. **File Upload Errors**
   - Check `MAX_CONTENT_LENGTH` setting
   - Verify upload directory permissions

2. **Memory Issues**
   - Increase Gunicorn worker memory
   - Implement file cleanup

3. **Permission Errors**
   - Check directory permissions
   - Ensure application user has write access

### Monitoring Commands
```bash
# Check application status
curl http://localhost:5000/health

# View logs
tail -f logs/app.log

# Monitor system resources
htop
```

## 📞 Support

For issues and support:
1. Check logs first
2. Review configuration
3. Consult this documentation
4. Contact system administrator

## 🔄 Updates

### Deployment Process
1. Test changes in development
2. Create pull request
3. Review and merge to main
4. CI/CD pipeline automatically deploys
5. Monitor application health

### Rollback Process
```bash
# Quick rollback
docker run -d previous-image-tag

# Or revert git commit
git revert HEAD
./deploy.sh
```
