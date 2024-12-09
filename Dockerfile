FROM python:3.8-slim-buster

WORKDIR /app

COPY requirement.txt requirement.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]