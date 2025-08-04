# Training Report Generator

A Flask web application for generating professional training report documents with image processing capabilities.

## 🚀 Features

- **Web Interface**: User-friendly form for training report data input
- **Document Generation**: Creates Word documents from customizable templates
- **Image Processing**: Handles galleries and annexure images
- **Multi-Template Support**: 5 different organizational templates (RRECL, GEDA, HAREDA, UREDA, SDA Odisha)
- **File Upload**: Secure file upload with validation
- **Responsive Design**: Works on desktop and mobile devices

## 📁 Project Structure

```
training-report-generator/
├── app_clean.py              # Main Flask application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── render.yaml              # Render deployment config
├── modules/                 # Custom modules
│   ├── document_utils.py    # Document processing utilities
│   ├── form_processing.py   # Form data handling
│   └── image_processing.py  # Image processing functions
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── output/                  # Generated reports
└── word_template_*.docx     # Word templates
```

## 🛠️ Installation & Setup

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd training-report-generator
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the application**
```bash
python app_clean.py
```

Visit `http://localhost:5000` to access the application.

## 🚀 Deployment

### Render Deployment (Recommended)

1. **Push to GitHub**
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

2. **Deploy on Render**
   - Connect your GitHub repository to Render
   - The `render.yaml` file will automatically configure the deployment
   - Set environment variables in Render dashboard

3. **Environment Variables for Production**
```
SECRET_KEY=your-super-secure-secret-key
FLASK_ENV=production
DEBUG=False
MAX_CONTENT_LENGTH=31457280
```

### Other Deployment Options

#### Heroku
```bash
# Install Heroku CLI and login
heroku create your-app-name
git push heroku main
```

#### Docker
```bash
# Build and run with Docker
docker build -t training-report-generator .
docker run -p 5000:5000 training-report-generator
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `dev-key-change-in-production` |
| `FLASK_ENV` | Environment mode | `development` |
| `DEBUG` | Debug mode | `False` |
| `MAX_CONTENT_LENGTH` | Max file upload size | `31457280` (30MB) |
| `UPLOAD_FOLDER` | Upload directory | `./static/uploads` |
| `OUTPUT_FOLDER` | Output directory | `./output` |

### Template Configuration

The application supports 5 different organizational templates:
1. **Template 1**: RRECL
2. **Template 2**: GEDA
3. **Template 3**: HAREDA
4. **Template 4**: UREDA
5. **Template 5**: SDA Odisha

## 📝 Usage

1. **Access the web interface** at your deployed URL
2. **Fill out the form** with training details
3. **Upload images** for gallery and annexures (optional)
4. **Select the appropriate template** for your organization
5. **Generate the report** and download the Word document

## 🔒 Security Features

- File upload validation and size limits
- CSRF protection ready
- Secure file handling
- Environment-based configuration
- Production-ready error handling

## 🧪 Testing

### Test Endpoints
- `/` - Main application
- `/test` - Server status check
- `/test-form` - Simple form for testing
- `/health` - Health check endpoint

### Run Tests
```bash
# Test the application locally
python app_clean.py
# Visit http://localhost:5000/test-form
```

## 📊 Monitoring

- Health check endpoint: `/health`
- Application logs available in production
- Error tracking via Flask error handlers

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure virtual environment is activated
   - Install requirements: `pip install -r requirements.txt`

2. **Template Not Found**
   - Verify all `word_template_*.docx` files are present
   - Check file permissions

3. **File Upload Issues**
   - Check `MAX_CONTENT_LENGTH` setting
   - Verify upload directory permissions

### Support

For issues and questions:
- Check the logs for error details
- Verify environment configuration
- Ensure all template files are present

## 📄 License

This project is licensed under the MIT License.
