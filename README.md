# 🔗 URL Shortener

A modern, feature-rich URL shortening service built with Django and Django REST Framework. Transform long URLs into short, shareable links with QR code generation and expiration management.

### 🌐 Live Demo
**Hosted on PythonAnywhere:** https://urlshortnerlevmas.pythonanywhere.com/

![Django](https://img.shields.io/badge/Django-5.2.5-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.16.1-blue.svg)
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **🔗 URL Shortening**: Convert long URLs into short, manageable links
- **📱 QR Code Generation**: Automatic QR code generation for each shortened URL
- **⏰ Expiration Management**: Set custom expiration dates (1-30 days)
- **📊 Click Tracking**: Monitor click counts for analytics
- **🎨 Modern Web Interface**: Clean, responsive frontend
- **🔒 Security**: Input validation and secure URL patterns
- **📝 Comprehensive Logging**: Request tracking and performance monitoring
- **🚀 Production Ready**: Configured for PythonAnywhere deployment

## 🏗️ Architecture

### Backend (Django + DRF)
- **Models**: URL storage with metadata
- **Serializers**: Data validation and QR code generation
- **Views**: RESTful API endpoints
- **Utils**: Base62 encoding for short URL generation

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript**: Async API interactions

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- pip or uv package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Levmas25/URLShortner.git
cd URLShortner
```

2. **Install dependencies**
```bash
# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -r requirements.txt
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Start development server**
```bash
python manage.py runserver
```

5. **Access the application**
- Web Interface: http://127.0.0.1:8000/
- API Documentation: http://127.0.0.1:8000/api/

## 📖 API Documentation

### Create Short URL
**POST** `/api/shorten/`

**Request Body:**
```json
{
    "original_url": "https://example.com/very-long-url",
    "days_alive": 7
}
```

**Response:**
```json
{
    "original_url": "https://example.com/very-long-url",
    "shorted_url": "http://127.0.0.1:8000/api/abc123",
    "creation_date": "2025-08-30",
    "expiration_date": "2025-09-06",
    "click_count": 0,
    "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

### Access Short URL
**GET** `/api/{short_code}/`

- Redirects to the original URL
- Increments click counter
- Returns 410 Gone if expired

**Example:**
```bash
curl -L http://127.0.0.1:8000/api/abc123/
# Redirects to original URL
```

## 🗂️ Project Structure

```
URLShortner/
├── URLShortner/           # Django project settings
│   ├── settings.py        # Main configuration
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py           # WSGI application
├── shortnerAPI/          # Core API application
│   ├── models.py         # Database models
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # API views
│   ├── urls.py           # API URL patterns
│   └── utils.py          # Helper functions
├── shortnerWeb/          # Frontend application
│   ├── templates/        # HTML templates
│   ├── static/           # CSS, JS, images
│   └── views.py          # Web views
├── static/               # Collected static files
├── pyproject.toml        # Project dependencies
└── README.md            # This file
```

## 🛠️ Configuration

### Environment Variables
```bash
# Development
DEBUG=True
SECRET_KEY=your-secret-key

# Production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

### Database
Default: SQLite (development)
Production: PostgreSQL/MySQL recommended

### Static Files
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

## 🔒 Security Features

- **Input Validation**: URL format validation
- **XSS Protection**: Content Security Policy headers
- **CSRF Protection**: Built-in Django CSRF middleware
- **Rate Limiting**: Configurable request limits
- **Secure URL Patterns**: Regex validation for short codes

## 📊 Monitoring & Logging

The application includes comprehensive logging:

- **Request Tracking**: HTTP method, path, response time
- **Error Logging**: Exception details with stack traces
- **Performance Monitoring**: Response time measurements
- **Security Events**: Invalid request patterns

Logs are written to `debug.log` with configurable levels.

## 🚀 Deployment

### PythonAnywhere

1. **Upload project files**
2. **Install dependencies**
   ```bash
   pip3.10 install --user django djangorestframework pillow qrcode
   ```
3. **Configure static files**
   ```bash
   python3.10 manage.py collectstatic
   ```
4. **Set up web app** in PythonAnywhere dashboard

### Docker (Optional)
```dockerfile
FROM python:3.12-slim
COPY . /app
WORKDIR /app
RUN pip install -e .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📈 Performance

- **Base62 Encoding**: Efficient short code generation
- **Database Indexing**: Optimized queries
- **Static File Serving**: CDN-ready configuration
- **Caching**: Redis support (configurable)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django REST Framework team
- QR Code generation library contributors
- PythonAnywhere hosting platform

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Levmas25/URLShortner/issues)
- **Documentation**: [Wiki](https://github.com/Levmas25/URLShortner/wiki)
- **Email**: support@urlshortener.com

---

**Made with ❤️ using Django**