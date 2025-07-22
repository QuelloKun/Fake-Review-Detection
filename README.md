# Fake Review Detection - FastAPI Migration

## Overview
This project has been successfully migrated from Flask to FastAPI, providing improved performance, modern API capabilities, and better development experience.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Activate virtual environment**
```bash
source new_venv/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📁 Project Structure
```
Fake-Review-Detection v2/
├── main.py                 # FastAPI application
├── classifierx.pickle    # ML model file
├── templates/              # HTML templates
│   ├── first.html         # Home page
│   ├── index.html         # Prediction form
│   └── login.html         # Login page
├── static/                # CSS, JS, images
└── requirements.txt       # Dependencies
```

## 🌐 Endpoints

### Web Interface
- `GET /` - Home page (first.html)
- `GET /login` - Login page
- `GET /index` - Prediction form
- `POST /predict` - Handle prediction form submission

### REST API
- `GET /api/predict` - Predict fake/real review
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## 🔧 API Usage

### Web Form Submission
Navigate to http://localhost:8000 and use the web interface.

### REST API Example
```bash
# Health check
curl http://localhost:8000/health

# Predict review
curl -X GET "http://localhost:8000/api/predict?review_text=Great%20product&rating=5&verified_purchase=Y&category=Electronics"
```

### API Parameters
- `review_text` (string): The review text to analyze
- `rating` (integer): Product rating (1-5)
- `verified_purchase` (string): "Y" or "N"
- `category` (string): Product category

### Response Format
```json
{
  "prediction": "Real",
  "confidence": 0.95
}
```

## 🛠️ Development

### Adding New Features
1. Edit `main.py` to add new endpoints
2. Update templates in `templates/` directory
3. Add new static files to `static/` directory

### Testing
```bash
# Run with auto-reload
uvicorn main:app --reload

# Run on different port
uvicorn main:app --port 8001
```

## 🔍 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Run on different port
uvicorn main:app --port 8001
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Model File Issues
Ensure `classifierx.pickle` exists in the project root directory.

## 📊 Performance Improvements
- **Async processing**: Non-blocking request handling
- **Type safety**: Pydantic validation
- **Auto-documentation**: Interactive API docs
- **Better error handling**: Structured error responses

## 🔄 Migration Notes
- All Flask routes have been converted to FastAPI
- Templates updated for FastAPI compatibility
- Static file serving configured
- Model loading optimized

## 🌟 Features
- ✅ Fake review detection using ML
- ✅ REST API with documentation
- ✅ Web interface
- ✅ Health monitoring
- ✅ Error handling
- ✅ Static file serving

## 📞 Support
For issues or questions, check the API documentation at http://localhost:8000/docs
