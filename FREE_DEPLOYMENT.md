# Free Server Deployment Guide

## 🆓 Railway Deployment (Recommended)

### Quick Setup:
1. **Visit**: https://railway.app
2. **Sign up** with GitHub account
3. **Create new project** → "Deploy from GitHub repo"
4. **Select** this repository
5. **Configure**:
   - Environment: `FLASK_ENV=production`
   - Port: Railway auto-configures
6. **Deploy** - Railway builds and deploys automatically!

### Environment Variables to Set:
```
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
MAX_CONTENT_LENGTH=31457280
```

---

## 🌐 Render.com Deployment

### Quick Setup:
1. **Visit**: https://render.com
2. **Connect GitHub** account
3. **New Web Service** → Connect repository
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app_clean:app --host 0.0.0.0 --port $PORT`
5. **Deploy**

---

## ⚡ Vercel Deployment

### Quick Setup:
1. **Visit**: https://vercel.com
2. **Import Git Repository**
3. **Configure**:
   - Framework: Other
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: (leave empty)
4. **Deploy**

---

## 🐍 PythonAnywhere Deployment

### Quick Setup:
1. **Visit**: https://pythonanywhere.com
2. **Create free account**
3. **Upload files** via Files tab
4. **Web tab** → Add new web app
5. **Configure WSGI file** to point to your app
6. **Reload** web app

---

## 📋 Pre-Deployment Checklist

✅ All files in repository
✅ requirements.txt updated
✅ Procfile created
✅ Environment variables ready
✅ DOCX templates included
✅ Static files in static/ folder

## 🔧 Troubleshooting

### Common Issues:
1. **File uploads not working**: Check file permissions
2. **Templates not found**: Ensure DOCX files are in root directory
3. **Static files 404**: Check static folder structure

### Debug Commands:
```bash
# Check if app starts locally
python app_clean.py

# Test requirements install
pip install -r requirements.txt

# Verify all files present
ls -la
```

## 🎯 Expected Results

After deployment, your app will be available at:
- Railway: `https://your-app-name.railway.app`
- Render: `https://your-app-name.onrender.com`
- Vercel: `https://your-app-name.vercel.app`

## 💡 Tips for Free Hosting

1. **Railway**: Best for Docker apps, $5 free credit monthly
2. **Render**: Most reliable, 750 hours/month free
3. **Vercel**: Fastest deployment, great performance
4. **PythonAnywhere**: Python-specific, easiest setup

Choose based on your preference - all will work great! 🚀
