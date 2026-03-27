FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader stopwords wordnet omw-1.4

COPY src/ src/
COPY models/ models/
# Note: In a real docker build, models might be downloaded or trained during build
# Here we copy the local model if it exists

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
