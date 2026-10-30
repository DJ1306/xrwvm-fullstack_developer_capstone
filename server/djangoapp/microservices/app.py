from pathlib import Path
import os
from flask import Flask,jsonify
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk.data
app=Flask(__name__)
lexicon=Path(__file__).parent/"sentiment"/"vader_lexicon.zip"
nltk.data.path.insert(0,str(Path(__file__).parent))
sia=SentimentIntensityAnalyzer(lexicon_file="sentiment/vader_lexicon.zip/vader_lexicon/vader_lexicon.txt")
@app.get("/")
def home():
    return jsonify(service="Sentiment Analyzer",status="ready")
@app.get("/analyze/<path:text>")
def analyze(text):
    score=sia.polarity_scores(text)["compound"]
    return jsonify(sentiment="positive" if score>=.05 else "negative" if score<=-.05 else "neutral")
if __name__=="__main__":
    app.run(host="127.0.0.1",port=int(os.getenv("PORT","5050")))
