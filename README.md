# Fake Review Detection System

A modern full-stack application that uses machine learning to detect fake Amazon reviews with high accuracy.

## 🚀 Features

- **AI-Powered Detection**: Advanced ML model using NLTK and scikit-learn
- **Modern Frontend**: React/Next.js with TypeScript and Tailwind CSS
- **Fast API Backend**: FastAPI with async PostgreSQL database
- **Real-time Analysis**: Instant review classification with confidence scores
- **Database Storage**: All predictions saved for analysis and tracking
- **Professional UI**: Clean, responsive design with modern components

## 🏗️ Architecture

```
├── app/                    # FastAPI Backend
│   ├── api/v1/            # API routes and schemas
│   ├── core/              # Configuration and security
│   ├── crud/              # Database operations
│   ├── db/                # Database setup
│   ├── models/            # SQLAlchemy models
│   └── services/          # ML service
├── frontend/              # Next.js Frontend
│   └── src/
│       └── app/           # Next.js App Router
├── models/                # ML model files
├── alembic/              # Database migrations
└── requirements.txt       # Python dependencies
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Production database
- **SQLAlchemy** - ORM with async support
- **Alembic** - Database migrations
- **NLTK & scikit-learn** - Machine learning pipeline

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Modern Components** - Clean, responsive UI

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL 15+
- Git

### 1. Clone Repository
```bash
git clone <repository-url>
cd Fake-Review-Detection\ v2
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv new_venv
source new_venv/bin/activate  # Linux/Mac
# new_venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL (using Docker)
docker compose up -d postgres redis

# Run database migrations
alembic upgrade head

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start development server
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 npm run dev -- --port 3000
```

### 4. Access Applications
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/api/v1/health

## 📱 Usage

1. **Open the frontend** at http://localhost:3000
2. **Enter review details**:
   - Review text (minimum 10 characters)
   - Product rating (1-5 stars)
   - Verified purchase status
   - Product category
3. **Click "Analyze Review"** to get instant results
4. **View prediction**: Real or Fake with confidence indicator

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/fake_reviews
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ML Model
MODEL_PATH=./models/
MODEL_NAME=classifierx.pickle
CACHE_TTL=3600

# API
API_V1_STR=/api/v1
PROJECT_NAME=Fake Review Detection API
VERSION=1.0.0
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000
```

## 🐳 Docker Deployment

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## 🧪 API Endpoints

### Health Check
```bash
GET /api/v1/health
```

### Predictions
```bash
POST /api/v1/predictions/
GET /api/v1/predictions/
GET /api/v1/predictions/{id}
```

### Authentication
```bash
POST /api/v1/auth/register
POST /api/v1/auth/login
```

## 🔍 ML Model Details

The system uses a trained machine learning pipeline that analyzes:
- **Review text patterns** using NLTK preprocessing
- **Rating consistency** with review sentiment
- **Purchase verification** status
- **Product category** context
- **Writing style** indicators

**Model Performance**:
- High accuracy on Amazon review datasets
- Confidence scoring for each prediction
- Continuous learning capability

## 🧑‍💻 Development

### Running Tests
```bash
# Backend tests
pytest

# Frontend tests
cd frontend && npm test
```

### Code Quality
```bash
# Python linting
flake8 app/
black app/

# TypeScript checking
cd frontend && npm run lint
```

## 📊 Database Schema

- **Users**: User accounts and authentication
- **Predictions**: Review analysis results with metadata
- **Alembic**: Migration version tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Links

- **Live Demo**: [Coming Soon]
- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

---

**Built with ❤️ using FastAPI, Next.js, and Machine Learning**
