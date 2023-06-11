FROM python:3.7-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_ENV=production

ENV FLASK_APP=app.py

CMD ["python", "./app/app.py"]