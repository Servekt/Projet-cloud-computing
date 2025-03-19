FROM python:3.10-alpine

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
EXPOSE 4123

CMD ["python", "app.py"]
