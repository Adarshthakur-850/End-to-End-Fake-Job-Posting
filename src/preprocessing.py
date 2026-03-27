import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Allow downloading implicitly if needed, though usually better in Dockerfile/setup
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # 3. Tokenize & Remove Stopwords & Lemmatize
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    
    return " ".join(tokens)

def combine_text_columns(df):
    # Combine relevant text columns into a single 'text' column
    text_cols = ['title', 'company_profile', 'description', 'requirements', 'benefits']
    
    # Fill NaN with empty string
    for col in text_cols:
        df[col] = df[col].fillna('')
        
    df['text'] = df[text_cols].apply(lambda x: ' '.join(x), axis=1)
    return df
