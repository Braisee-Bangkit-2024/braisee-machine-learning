# Gunakan base image yang spesifik
FROM python:3.9-bullseye

# Set environment variables untuk best practice
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instal dependensi sistem
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Buat user non-root untuk keamanan
RUN addgroup --system app && adduser --system --group app
USER app

# Salin sisa kode aplikasi
COPY . .

# Expose port (hanya untuk dokumentasi, Cloud Run tidak menggunakan ini)
EXPOSE 8080

# CMD yang patuh pada platform Cloud
# Ini adalah baris paling krusial
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}"]
