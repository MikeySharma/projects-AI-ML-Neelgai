
import joblib
from utils.preprocess import  * 
import numpy as np

# Load SVM model for news classification
model = joblib.load('models/news_clasification.pkl')
tfidf = joblib.load('models/tfidf.pkl')

# news class
category_class = ['business', 'entertainment', 'politics', 'sport', 'tech']

def classify_news(news):

    processed_news = preprocess(news)
    news_encoding = tfidf.transform([processed_news]).toarray()
    
    
    confidence = model.predict_proba(news_encoding)
    index = np.argmax(confidence)
    confidence = max(np.around(x * 100, 2) for x in confidence)
    return f"The provided news text is classified as '{category_class[int(index)].upper()}' with {max(confidence)}% confidence"