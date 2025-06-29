FROM python:3.9-slim AS builder

# Set variabel lingkungan agar Python tidak membuat file .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Set variabel lingkungan agar output Python tidak di-buffer
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instal dependensi sistem terlebih dahulu
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Salin HANYA file requirements.txt terlebih dahulu
COPY requirements.txt .

# Instal dependensi Python. Ini akan di-cache selama requirements.txt tidak berubah
RUN pip install --no-cache-dir -r requirements.txt

# =================================================================
# Tahap 2: Final - Image akhir yang bersih dan ringan
# =================================================================
FROM python:3.9-slim

WORKDIR /app

# Buat user baru yang tidak punya hak istimewa
RUN addgroup --system app && adduser --system --group app

# Salin dependensi sistem dari tahap builder
COPY --from=builder /etc/ssl/certs /etc/ssl/certs
COPY --from=builder /usr/share/doc /usr/share/doc
COPY --from=builder /usr/share/glib-2.0 /usr/share/glib-2.0
COPY --from=builder /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu

# Salin virtual environment dari tahap builder
COPY --from=builder /app /app

# Salin sisa kode aplikasi
COPY . .

# Berikan kepemilikan folder kepada user baru kita
RUN chown -R app:app /app

# Ganti ke user baru
USER app

# Expose port
EXPOSE 8080

# Jalankan aplikasi (gunakan exec form yang lebih bersih)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
