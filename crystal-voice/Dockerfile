FROM python:3.9-slim

WORKDIR /app

COPY ./crystal-voice /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50051

CMD ["python", "voice-app.py"]