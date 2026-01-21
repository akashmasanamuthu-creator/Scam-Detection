import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from preprocessing import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset.csv")

data = pd.read_csv(DATASET_PATH)
data["cleaned"] = data["message"].apply(clean_text)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data["cleaned"])
y = data["label"]

model = LogisticRegression()
model.fit(X, y)

def predict_message(text):
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    probability = round(model.predict_proba(vector)[0][1] * 100, 2)
    return prediction, probability
