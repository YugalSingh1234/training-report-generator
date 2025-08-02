# Complete Server Deployment Guide

## Overview
This guide provides step-by-step instructions for deploying the Training Report Generator application to a production server.

## Prerequisites
- Ubuntu 20.04+ or Debian 10+ server
- Domain name pointed to your server
- SSH access to the server
- Minimum 2GB RAM, 20GB storage

## Quick Deployment Steps

### 1. Prepare Your Server

#### Option A: Cloud Providers (Recommended)

**DigitalOcean (Recommended for beginners)**
```bash
# Create a droplet with:
# - Ubuntu 22.04 LTS
# - 2GB RAM minimum
# - SSH key authentication
# - Enable monitoring and backups
```

**AWS EC2**
```bash
# Launch instance with:
# - Ubuntu 22.04 LTS AMI
# - t3.small or larger
# - Security group allowing ports 22, 80, 443
# - Elastic IP address
```

**Google Cloud Platform**
```bash
# Create VM instance with:
# - Ubuntu 22.04 LTS
# - e2-small or larger
# - Allow HTTP/HTTPS traffic
# - Static external IP
```

#### Option B: VPS Providers
- Linode, Vultr, Hetzner, OVH
- Similar specifications as above

### 2. Initial Server Setup

Connect to your server via SSH:
```bash
ssh root@your-server-ip
# or
ssh ubuntu@your-server-ip
```

### 3. Upload Your Code

#### Method 1: Git (Recommended)
```bash
# On your local machine, push to GitHub/GitLab
git add .
git commit -m "Production deployment"
git push origin main

# On server
git clone https://github.com/yourusername/word-generator.git
cd word-generator
```

#### Method 2: SCP Upload
```bash
# On your local machine
scp -r /path/to/Word_Generator_Project ubuntu@your-server-ip:/home/ubuntu/
```

#### Method 3: SFTP/File Manager
Use tools like FileZilla, WinSCP, or VS Code's SFTP extension to upload files.

### 4. Run Automated Deployment

Make the deployment script executable and run it:
```bash
chmod +x server_deploy.sh
sudo ./server_deploy.sh
```

The script will automatically:
- Update system packages
- Install Docker and Docker Compose
- Set up firewall rules
- Configure SSL certificates
- Start the application
- Set up monitoring and backups

### 5. Configure Your Domain

#### DNS Configuration
Point your domain to your server:
```
Type: A
Name: @ (or your subdomain)
Value: your-server-ip
TTL: 300
```

For subdomains:
```
Type: A
Name: app (for app.yourdomain.com)
Value: your-server-ip
TTL: 300
```

#### SSL Certificate
The deployment script automatically configures Let's Encrypt SSL certificates.

### 6. Final Configuration

#### Update Environment Variables
```bash
cd /opt/word-generator
sudo nano .env

# Update these values:
SECRET_KEY=your-actual-secret-key
SERVER_NAME=yourdomain.com
MAIL_USERNAME=your-email@domain.com
MAIL_PASSWORD=your-app-password
```

#### Restart Services
```bash
sudo docker-compose restart
```

## Post-Deployment Checklist

### 1. Verify Installation
```bash
# Check if containers are running
sudo docker ps

# Check application logs
sudo docker-compose logs app

# Test the application
curl http://localhost
curl https://yourdomain.com
```

### 2. Test Functionality
- [ ] Access the web interface
- [ ] Upload test images
- [ ] Generate a test report
- [ ] Verify file downloads work
- [ ] Check email notifications (if configured)

### 3. Security Verification
```bash
# Check firewall status
sudo ufw status

# Verify SSL certificate
sudo certbot certificates

# Check security headers
curl -I https://yourdomain.com
```

### 4. Performance Testing
```bash
# Check system resources
htop
df -h
free -h

# Test application performance
ab -n 100 -c 10 https://yourdomain.com/
```

## Monitoring and Maintenance

### 1. Application Monitoring
- Access monitoring dashboard: `https://yourdomain.com/monitoring`
- Check logs: `sudo docker-compose logs -f`
- System metrics: `htop`, `iotop`, `nethogs`

### 2. Regular Maintenance
```bash
# Update system packages (monthly)
sudo apt update && sudo apt upgrade -y

# Update Docker images (as needed)
sudo docker-compose pull
sudo docker-compose up -d

# Backup data (automated daily)
# Backups are stored in /opt/backups/
ls -la /opt/backups/

# Renew SSL certificates (automatic via cron)
sudo certbot renew --dry-run
```

### 3. Log Management
```bash
# Application logs
sudo docker-compose logs app --tail=100

# Nginx logs
sudo docker-compose logs nginx --tail=100

# System logs
sudo journalctl -u docker -f
```

## Troubleshooting

### Common Issues

#### 1. Application Not Starting
```bash
# Check Docker status
sudo systemctl status docker

# Check container logs
sudo docker-compose logs app

# Restart services
sudo docker-compose restart
```

#### 2. SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Renew certificates manually
sudo certbot renew

# Check Nginx configuration
sudo docker-compose exec nginx nginx -t
```

#### 3. Permission Issues
```bash
# Fix file permissions
sudo chown -R 1000:1000 /opt/word-generator/static/uploads
sudo chown -R 1000:1000 /opt/word-generator/output
```

#### 4. High Memory Usage
```bash
# Check resource usage
sudo docker stats

# Restart containers if needed
sudo docker-compose restart

# Check for memory leaks
sudo docker-compose logs app | grep -i memory
```

### Performance Optimization

#### 1. Enable Caching
```bash
# Redis is already configured in docker-compose.yml
# Monitor Redis usage
sudo docker-compose exec redis redis-cli info memory
```

#### 2. Optimize Nginx
```bash
# Nginx configuration is already optimized in nginx.conf
# Monitor Nginx performance
sudo docker-compose logs nginx | grep -E "GET|POST"
```

#### 3. Database Optimization (if added later)
```bash
# Monitor database performance
# Implement connection pooling
# Regular maintenance tasks
```

## Scaling Considerations

### 1. Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Multiple application containers
- Shared storage for uploads
- External database

### 2. Vertical Scaling
- Increase server resources
- Optimize Docker memory limits
- Monitor and adjust based on usage

### 3. CDN Integration
- CloudFlare, AWS CloudFront
- Serve static files from CDN
- Reduce server load

## Backup and Recovery

### 1. Automated Backups
- Daily backups are configured automatically
- Backups include: application data, uploads, configuration
- Retention: 7 daily, 4 weekly, 12 monthly

### 2. Manual Backup
```bash
# Create manual backup
sudo /opt/scripts/backup.sh

# Restore from backup
sudo /opt/scripts/restore.sh /opt/backups/backup-YYYY-MM-DD.tar.gz
```

### 3. Disaster Recovery
- Keep backups in multiple locations
- Test recovery procedures regularly
- Document recovery process

## Security Best Practices

### 1. Regular Updates
- Keep system packages updated
- Update Docker images regularly
- Monitor security advisories

### 2. Access Control
- Use SSH keys instead of passwords
- Implement fail2ban for brute force protection
- Regular security audits

### 3. Monitoring
- Set up log monitoring
- Implement intrusion detection
- Regular security scans

## Support and Maintenance

### 1. Monitoring Alerts
- Set up email notifications for issues
- Monitor disk space, memory, CPU
- Application error tracking

### 2. Regular Maintenance Tasks
- Weekly log rotation
- Monthly security updates
- Quarterly performance reviews

### 3. Emergency Procedures
- Contact information for support
- Emergency shutdown procedures
- Disaster recovery contacts

## Cost Estimation

### Monthly Costs (USD)

**Small Setup (2GB RAM, 50GB SSD)**
- DigitalOcean: $12/month
- AWS t3.small: ~$15/month
- Google Cloud e2-small: ~$13/month

**Medium Setup (4GB RAM, 80GB SSD)**
- DigitalOcean: $24/month
- AWS t3.medium: ~$30/month
- Google Cloud e2-medium: ~$27/month

**Additional Costs**
- Domain name: $10-15/year
- SSL certificate: Free (Let's Encrypt)
- Backup storage: $2-5/month
- Monitoring tools: Free (included)

## Getting Help

### 1. Log Analysis
- Check application logs first
- Review system logs
- Analyze error patterns

### 2. Community Support
- Stack Overflow for technical issues
- Docker documentation
- Flask community forums

### 3. Professional Support
- Cloud provider support plans
- DevOps consulting services
- Application maintenance contracts

---

## Next Steps After Deployment

1. **Set up monitoring alerts**
2. **Configure backup notifications**
3. **Implement CI/CD pipeline**
4. **Add database if needed**
5. **Set up staging environment**
6. **Plan for scaling**

Your Training Report Generator is now ready for production use! 🚀

For questions or issues, refer to the troubleshooting section or check the application logs.
