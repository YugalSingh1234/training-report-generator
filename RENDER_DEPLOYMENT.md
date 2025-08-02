# Render.com Deployment Guide
## Training Report Generator

### 🚀 **Quick Deployment Steps**

#### **Phase 1: Prepare Repository**

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Prepared for Render deployment"
   git push origin main
   ```

#### **Phase 2: Render.com Setup**

1. **Visit**: https://render.com
2. **Sign Up/Login** with your GitHub account
3. **Click "New +"** → **"Web Service"**
4. **Connect Repository**:
   - Select your GitHub repository
   - Choose "Word_Generator_Project" repo

#### **Phase 3: Configure Service**

1. **Basic Settings**:
   - **Name**: `training-report-generator` (or your choice)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty

2. **Build & Deploy Settings**:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app_clean:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables** (Add these):
   ```
   FLASK_ENV=production
   SECRET_KEY=your-random-secret-key-here
   MAX_CONTENT_LENGTH=31457280
   PYTHONPATH=.
   ```

4. **Advanced Settings**:
   - **Auto-Deploy**: Yes
   - **Health Check Path**: `/health`

#### **Phase 4: Deploy**

1. **Click "Create Web Service"**
2. **Wait for build** (takes 3-5 minutes)
3. **Check logs** for any errors
4. **Test your app** at the provided URL

---

### 📋 **Detailed Step-by-Step Process**

#### **Step 1: GitHub Repository Setup**

```bash
# Make sure your code is in GitHub
git status
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

#### **Step 2: Render.com Account**

1. Go to **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub account**
4. Authorize Render to access your repositories

#### **Step 3: Create Web Service**

1. **Dashboard** → Click **"New +"**
2. Select **"Web Service"**
3. **Connect a repository**:
   - Choose your GitHub account
   - Select "Word_Generator_Project" repository
   - Click **"Connect"**

#### **Step 4: Configure Your Service**

**Basic Info:**
```
Name: training-report-generator
Region: Oregon (US West) or Frankfurt (Europe)
Branch: main
Root Directory: (leave empty)
```

**Build Settings:**
```
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app_clean:app --host 0.0.0.0 --port $PORT
```

**Environment Variables:**
Click **"Add Environment Variable"** for each:
```
Key: FLASK_ENV          Value: production
Key: SECRET_KEY         Value: your-secret-key-change-this
Key: MAX_CONTENT_LENGTH Value: 31457280
Key: PYTHONPATH         Value: .
```

**Advanced Settings:**
```
Auto-Deploy: Yes (deploys automatically on git push)
Health Check Path: /health
```

#### **Step 5: Deploy & Test**

1. **Click "Create Web Service"**
2. **Monitor build logs**:
   - Build process starts automatically
   - Watch for any error messages
   - Usually takes 3-5 minutes

3. **Get your URL**:
   - Render provides: `https://your-app-name.onrender.com`
   - URL appears once deployment is successful

4. **Test your application**:
   - Visit the URL
   - Try uploading an image
   - Generate a test report
   - Download the generated document

---

### 🔧 **Environment Variables Explained**

| Variable | Value | Purpose |
|----------|--------|---------|
| `FLASK_ENV` | `production` | Sets Flask to production mode |
| `SECRET_KEY` | `your-secret-key` | Flask session security |
| `MAX_CONTENT_LENGTH` | `31457280` | 30MB file upload limit |
| `PYTHONPATH` | `.` | Helps Python find modules |

---

### 🚨 **Troubleshooting Common Issues**

#### **1. Build Fails**
**Error**: `pip install` fails
**Solution**: Check requirements.txt, remove problematic packages

#### **2. App Won't Start**
**Error**: Application timeout
**Solution**: Check start command, ensure gunicorn is in requirements.txt

#### **3. File Uploads Don't Work**
**Error**: Permission denied
**Solution**: Render handles file permissions automatically

#### **4. DOCX Templates Not Found**
**Error**: Template file not found
**Solution**: Ensure .docx files are committed to git and in root directory

#### **5. Static Files 404**
**Error**: CSS/JS not loading
**Solution**: Check static/ folder structure

---

### 📊 **Expected Results**

✅ **Successful Deployment Indicators:**
- Build completes without errors
- Service shows "Live" status
- Health check returns 200 OK
- Application loads at provided URL

✅ **Your App URL Will Be:**
```
https://training-report-generator.onrender.com
```
(or whatever name you choose)

✅ **Features Working:**
- Form submission
- Image uploads (up to 30MB)
- Document generation
- File downloads
- All 5 organization templates

---

### 💡 **Render.com Free Tier Benefits**

- ✅ **750 hours/month** (enough for always-on)
- ✅ **Automatic SSL** certificates
- ✅ **Custom domains** supported
- ✅ **Git-based deployments**
- ✅ **Environment variables**
- ✅ **Health checks**
- ✅ **Log viewing**
- ✅ **Auto-deploy** on git push

---

### 🎯 **Next Steps After Deployment**

1. **Test thoroughly** with real data
2. **Share the URL** with users
3. **Monitor usage** in Render dashboard
4. **Set up custom domain** (optional)
5. **Configure auto-deploy** for easy updates

---

### 📞 **Need Help?**

- **Render Docs**: https://render.com/docs
- **Build Logs**: Check in Render dashboard
- **App Logs**: View real-time in dashboard
- **Support**: Render has excellent documentation

Your Training Report Generator will be live and accessible worldwide! 🌍🚀
