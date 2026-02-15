import os
import pandas as pd
import re
import numpy as np
from urllib.parse import urlparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from preprocessing import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset.csv")
URL_DATASET_PATH = os.path.join(BASE_DIR, "url_dataset.csv")

# Message Model Training
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
    prediction = int(model.predict(vector)[0])
    probability = float(round(model.predict_proba(vector)[0][1] * 100, 2))
    return prediction, probability

# URL Scam Detection
SUSPICIOUS_KEYWORDS = [
    'verify', 'confirm', 'secure', 'urgent', 'update', 'action',
    'login', 'signin', 'account', 'claim', 'click', 'validate',
    'confirm-identity', 'check-account', 'unusual-activity'
]

SUSPICIOUS_TLDS = [
    '.tk', '.ml', '.ga', '.cf', '.pw', '.xyz', '.download',
    '.review', '.cricket', '.stream', '.gdn', '.best'
]

def extract_url_features(url):
    """Extract features from URL for scam detection"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        query = parsed.query
        
        features = {}
        
        # 1. URL length
        features['url_length'] = len(url)
        features['long_url'] = 1 if len(url) > 75 else 0
        
        # 2. Domain analysis
        features['dot_count'] = domain.count('.')
        features['dash_in_domain'] = 1 if '-' in domain else 0
        features['digits_in_domain'] = 1 if any(c.isdigit() for c in domain) else 0
        
        # 3. IP address check
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        features['has_ip'] = 1 if re.search(ip_pattern, domain) else 0
        
        # 4. Special characters
        features['special_chars'] = len(re.findall(r'[!@#$%^&*()_+=\[\]{};:\'",<>?/\\|`~-]', url))
        
        # 5. URL encoding
        features['percent_encoding'] = url.count('%')
        
        # 6. Port number
        features['has_port'] = 1 if ':' in domain and not '.com:' in url else 0
        
        # 7. Query string length
        features['query_length'] = len(query)
        features['has_query'] = 1 if query else 0
        
        # 8. Path depth
        features['path_depth'] = path.count('/')
        
        # 9. Suspicious keywords
        full_url_lower = url.lower()
        features['has_suspicious_keyword'] = 1 if any(keyword in full_url_lower for keyword in SUSPICIOUS_KEYWORDS) else 0
        
        # 10. Suspicious TLD
        features['has_suspicious_tld'] = 1 if any(url.endswith(tld) for tld in SUSPICIOUS_TLDS) else 0
        
        # 11. WWW count
        features['www_count'] = url.count('www')
        
        # 12. HTTPS vs HTTP
        features['uses_https'] = 1 if url.startswith('https') else 0
        
        # 13. Subdomain count
        features['subdomain_count'] = domain.count('.') - 1 if domain.count('.') > 0 else 0
        
        # 14. Domain length
        features['domain_length'] = len(domain)
        
        return features
    except:
        return {}

def convert_features_to_array(features):
    """Convert feature dict to numpy array"""
    feature_keys = ['url_length', 'long_url', 'dot_count', 'dash_in_domain', 
                    'digits_in_domain', 'has_ip', 'special_chars', 'percent_encoding',
                    'has_port', 'query_length', 'has_query', 'path_depth',
                    'has_suspicious_keyword', 'has_suspicious_tld', 'www_count',
                    'uses_https', 'subdomain_count', 'domain_length']
    
    return np.array([features.get(key, 0) for key in feature_keys]).reshape(1, -1)

# URL Model Training
try:
    url_data = pd.read_csv(URL_DATASET_PATH)
    
    # Extract features for all URLs
    url_features_list = []
    for url in url_data['url']:
        features = extract_url_features(url)
        url_features_list.append(features)
    
    # Convert to feature matrix
    feature_keys = ['url_length', 'long_url', 'dot_count', 'dash_in_domain', 
                    'digits_in_domain', 'has_ip', 'special_chars', 'percent_encoding',
                    'has_port', 'query_length', 'has_query', 'path_depth',
                    'has_suspicious_keyword', 'has_suspicious_tld', 'www_count',
                    'uses_https', 'subdomain_count', 'domain_length']
    
    X_url = np.array([[f.get(key, 0) for key in feature_keys] for f in url_features_list])
    y_url = url_data['label'].values
    
    # Scale features
    url_scaler = StandardScaler()
    X_url_scaled = url_scaler.fit_transform(X_url)
    
    # Train URL model
    url_model = RandomForestClassifier(n_estimators=100, random_state=42)
    url_model.fit(X_url_scaled, y_url)
    
except Exception as e:
    print(f"Error loading URL dataset: {e}")
    url_model = None
    url_scaler = None

def predict_url(url):
    """Predict if URL is a scam using trained model"""
    features = extract_url_features(url)
    
    if not features:
        return 0, 10.0  # Default to safe if parsing fails
    
    try:
        # Use trained model if available
        if url_model is not None and url_scaler is not None:
            X_features = convert_features_to_array(features)
            X_scaled = url_scaler.transform(X_features)
            
            prediction = int(url_model.predict(X_scaled)[0])
            probability = float(round(url_model.predict_proba(X_scaled)[0][1] * 100, 2))
            
            return prediction, probability
    except Exception as e:
        print(f"Error in model prediction: {e}")
    
    # Fallback to heuristic scoring if model fails
    return predict_url_heuristic(features)

def predict_url_heuristic(features):
    """Fallback heuristic-based URL scam detection"""
    scam_score = 0
    
    # High weight features
    scam_score += features.get('has_ip', 0) * 30
    scam_score += features.get('has_suspicious_keyword', 0) * 20
    scam_score += features.get('has_suspicious_tld', 0) * 25
    scam_score += features.get('long_url', 0) * 15
    
    # Medium weight features
    scam_score += features.get('dot_count', 0) * 3
    scam_score += features.get('dash_in_domain', 0) * 10
    scam_score += features.get('special_chars', 0) * 2
    scam_score += features.get('percent_encoding', 0) * 5
    scam_score += features.get('has_port', 0) * 15
    
    scam_score += features.get('digits_in_domain', 0) * 5
    scam_score -= features.get('uses_https', 0) * 20
    
    probability = float(min(100, max(0, scam_score)))
    prediction = 1 if probability >= 40 else 0
    
    return int(prediction), float(probability)
