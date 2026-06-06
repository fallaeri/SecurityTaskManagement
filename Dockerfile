FROM python:3.12-slim

# Security: don't run as root
RUN addgroup --system app && adduser --system --group app

WORKDIR /app

# Install system dependency for python-magic
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p media staticfiles && chown -R app:app /app

USER app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
