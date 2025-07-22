from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from typing import Optional
import os

# Initialize FastAPI app
app = FastAPI(title="Fake Review Detection API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Load the classifier
MODEL_PATH = "classifierx.pickle"
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        classifier = pickle.load(f)
else:
    raise FileNotFoundError(f"Model file {MODEL_PATH} not found")

# Initialize preprocessing components
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
table = str.maketrans({key: None for key in string.punctuation})

def preProcess(text):
    """Preprocess text for prediction"""
    filtered_tokens = []
    lemmatized_tokens = []
    text = text.translate(table)
    for w in text.split(" "):
        if w not in stop_words:
            lemmatized_tokens.append(lemmatizer.lemmatize(w.lower()))
        filtered_tokens = [' '.join(l) for l in nltk.bigrams(lemmatized_tokens)] + lemmatized_tokens
    return filtered_tokens

def toFeatureVector(Rating, verified_Purchase, product_Category, tokens):
    """Convert input to feature vector"""
    featureDict = {}
    localDict = {}
    
    featureDict["R"] = 1   
    localDict["R"] = Rating

    featureDict["VP"] = 1
    localDict["VP"] = 1 if verified_Purchase == "Y" else 0

    if product_Category not in featureDict:
        featureDict[product_Category] = 1
    else:
        featureDict[product_Category] = +1
            
    if product_Category not in localDict:
        localDict[product_Category] = 1
    else:
        localDict[product_Category] = +1
            
    for token in tokens:
        if token not in featureDict:
            featureDict[token] = 1
        else:
            featureDict[token] = +1
            
        if token not in localDict:
            localDict[token] = 1
        else:
            localDict[token] = +1
    
    return localDict

# Pydantic models
class PredictionRequest(BaseModel):
    review_text: str
    rating: int
    verified_purchase: str
    category: str

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float

@app.get("/", response_class=HTMLResponse)
async def first(request: Request):
    """Home page"""
    return templates.TemplateResponse("first.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    """Index page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    news: str = Form(...),
    rating: int = Form(...),
    verified_options: str = Form(...),
    category_options: str = Form(...)
):
    """Handle prediction form submission"""
    try:
        # Preprocess the input
        input_data = news.rstrip()
        rating_str = str(rating)
        
        # Create feature vector
        xfTestData = []
        xfTestData.append((toFeatureVector(rating_str, verified_options, category_options, preProcess(input_data)), rating_str))
        
        # Make prediction
        prediction = classifier.classify_many(map(lambda t: t[0], xfTestData))
        
        if prediction[0] == 1:
            result = "Real"
        else:
            result = "Fake"
        
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request,
                "prediction_text": f"Review is {result}"
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "prediction_text": f"Error: {str(e)}"
            }
        )

@app.get("/api/predict")
async def api_predict(
    review_text: str,
    rating: int,
    verified_purchase: str,
    category: str
):
    """REST API endpoint for prediction"""
    try:
        input_data = review_text.rstrip()
        rating_str = str(rating)
        
        xfTestData = []
        xfTestData.append((toFeatureVector(rating_str, verified_purchase, category, preProcess(input_data)), rating_str))
        
        prediction = classifier.classify_many(map(lambda t: t[0], xfTestData))
        
        result = "Real" if prediction[0] == 1 else "Fake"
        
        return {
            "prediction": result,
            "confidence": 0.95  # You can enhance this with actual confidence scores
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": classifier is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
