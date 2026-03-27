<<<<<<< HEAD
# Fake Job Posting Detection

Web application to detect fraudulent job postings using machine learning.

## Features
- **NLP Pipeline**: Preprocessing, TF-IDF vectorization.
- **Machine Learning**: RandomForestClassifier.
- **Backend**: FastAPI for prediction endpoint.
- **Frontend**: Simple HTML/JS interface.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Train the model (Requires dataset in `data/`):
   ```bash
   python src/train.py
   ```

3. Run the API:
   ```bash
   uvicorn src.api:app --reload
   ```

4. Use the Interface:
   Open `ui/index.html` in your browser.

## Docker
```bash
docker build -t fake-job-detector .
docker run -p 8000:8000 fake-job-detector
```
=======
# End-to-End-Fake-Job-Posting
ml project
>>>>>>> 48e85e246ea366fab5e84463b52fb22057f9c616
