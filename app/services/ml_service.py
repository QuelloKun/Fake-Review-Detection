import os
import pickle
import logging
from typing import Tuple, Optional
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

from app.core.config import settings

logger = logging.getLogger(__name__)


class MLService:
    def __init__(self):
        self.classifier = None
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.table = str.maketrans({key: None for key in string.punctuation})
        self._load_model()

    def _load_model(self):
        """Load the ML model from disk"""
        try:
            model_path = os.path.join(settings.MODEL_PATH, settings.MODEL_NAME)
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    self.classifier = pickle.load(f)
                logger.info("ML model loaded successfully")
            else:
                logger.error(f"Model file not found: {model_path}")
                raise FileNotFoundError(f"Model file {model_path} not found")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def _preprocess_text(self, text: str) -> list:
        """Preprocess text for prediction"""
        filtered_tokens = []
        lemmatized_tokens = []
        text = text.translate(self.table)
        
        for w in text.split(" "):
            if w.lower() not in self.stop_words:
                lemmatized_tokens.append(self.lemmatizer.lemmatize(w.lower()))
        
        filtered_tokens = [' '.join(l) for l in nltk.bigrams(lemmatized_tokens)] + lemmatized_tokens
        return filtered_tokens

    def _create_feature_vector(
        self,
        rating: str,
        verified_purchase: bool,
        product_category: str,
        tokens: list
    ) -> dict:
        """Convert input to feature vector"""
        feature_dict = {}
        
        feature_dict["R"] = 1
        feature_dict["VP"] = 1 if verified_purchase else 0
        
        if product_category not in feature_dict:
            feature_dict[product_category] = 1
        else:
            feature_dict[product_category] += 1
            
        for token in tokens:
            if token not in feature_dict:
                feature_dict[token] = 1
            else:
                feature_dict[token] += 1
        
        return feature_dict

    def predict(
        self,
        review_text: str,
        rating: int,
        verified_purchase: bool,
        category: str
    ) -> Tuple[str, Optional[float]]:
        """Make prediction using the ML model"""
        try:
            if not self.classifier:
                raise ValueError("Model not loaded")

            # Preprocess the input
            input_data = review_text.rstrip()
            rating_str = str(rating)
            
            # Create feature vector
            tokens = self._preprocess_text(input_data)
            feature_vector = self._create_feature_vector(
                rating_str,
                verified_purchase,
                category,
                tokens
            )
            
            # Make prediction
            prediction = self.classifier.classify_many([feature_vector])
            
            result = "real" if prediction[0] == 1 else "fake"
            confidence = 0.85  # Placeholder - can be enhanced with actual confidence scores
            
            return result, confidence
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise

    def health_check(self) -> bool:
        """Check if the model is loaded and ready"""
        return self.classifier is not None


# Initialize the ML service
ml_service = MLService()

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
