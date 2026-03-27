from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
from src.preprocessing import clean_text

app = FastAPI(title="Fake Job Detection API")

# Enable CORS for UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "models/job_classifier.pkl"
model = None

class JobPosting(BaseModel):
    text: str

@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model loaded.")
    else:
        print("Warning: Model file not found. Please train the model first.")

@app.post("/predict")
def predict(job: JobPosting):
    if not model:
        raise HTTPException(status_code=503, detail="Model is not loaded")
    
    processed_text = clean_text(job.text)
    prediction = model.predict([processed_text])[0]
    proba = model.predict_proba([processed_text])[0]
    
    label = "Fake" if prediction == 1 else "Real"
    confidence = float(proba[1] if prediction == 1 else proba[0])
    
    return {
        "label": label,
        "confidence": round(confidence * 100, 2)
    }

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}
