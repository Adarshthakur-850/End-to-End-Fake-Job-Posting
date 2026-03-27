import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from src.preprocessing import clean_text, combine_text_columns

DATA_PATH = "data/fake_job_postings.csv"
MODEL_PATH = "models/job_classifier.pkl"

def train_model():
    if not os.path.exists(DATA_PATH):
        print(f"Error: Dataset not found at {DATA_PATH}")
        return

    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    print("Preprocessing data...")
    df = combine_text_columns(df)
    df['clean_text'] = df['text'].apply(clean_text)
    
    X = df['clean_text']
    y = df['fraudulent']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Training model...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    pipeline.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Save Model
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    
    # Visualization
    visualize_results(y_test, y_pred, df)

def visualize_results(y_test, y_pred, df):
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.title("Confusion Matrix")
    plt.savefig("models/confusion_matrix.png")
    print("Saved confusion matrix plot.")
    
    # Word Clouds
    fake_text = " ".join(df[df['fraudulent'] == 1]['clean_text'])
    real_text = " ".join(df[df['fraudulent'] == 0]['clean_text'])
    
    if fake_text:
        wc_fake = WordCloud(width=800, height=400, background_color='black').generate(fake_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc_fake, interpolation='bilinear')
        plt.axis('off')
        plt.title("Fake Job Postings Word Cloud")
        plt.savefig("models/wordcloud_fake.png")
        
    if real_text:
        wc_real = WordCloud(width=800, height=400, background_color='white').generate(real_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc_real, interpolation='bilinear')
        plt.axis('off')
        plt.title("Real Job Postings Word Cloud")
        plt.savefig("models/wordcloud_real.png")

if __name__ == "__main__":
    train_model()
