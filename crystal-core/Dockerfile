FROM python:3.9-slim

WORKDIR /app

COPY crystal-core/core-app.py /app/
COPY crystal-core/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5005

CMD ["python", "core-app.py"]