FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fetch_recommendations.py /app/fetch_recommendations.py

WORKDIR /app

RUN chmod +x fetch_recommendations.py

CMD ["python", "-u", "fetch_recommendations.py"]