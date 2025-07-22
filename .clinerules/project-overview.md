## Brief overview
This project is a fake review detection system that has been migrated from Flask to FastAPI. It uses machine learning to classify Amazon reviews as real or fake based on review text, rating, verified purchase status, and product category.

## Communication style
- Keep responses concise and technical
- Focus on implementation details over theory
- Provide working code examples when requested
- Use bullet points for technical specifications

## Development workflow
- Use step-by-step approach for migrations
- Test each component before proceeding
- Use uvicorn for development server
- Prefer single-file implementations for simple features

## Coding best practices
- Use FastAPI for all new API development
- Use Pydantic models for request/response validation
- Maintain backward compatibility with existing templates
- Use async/await for database operations
- Include health check endpoints for monitoring

## Project context
- **Backend**: FastAPI with Python 3.12
- **ML Model**: classifierx.pickle (NLTK-based classifier)
- **Frontend**: Jinja2 templates with Bootstrap
- **Dependencies**: FastAPI, Uvicorn, NLTK, scikit-learn
- **Port**: 8001 (development)

## Other guidelines
- Always check for port conflicts before starting server
- Use new_venv virtual environment
- Include comprehensive error handling
- Document API endpoints with docstrings
- Use semantic commit messages (feat:, fix:, docs:)
