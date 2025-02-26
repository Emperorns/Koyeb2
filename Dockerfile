FROM python:3.9-slim

# Install Koyeb CLI
RUN apt-get update && apt-get install -y curl && \
    curl -s https://cli.koyeb.com/install.sh | bash

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "120", "app.main:app"]
