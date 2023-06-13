FROM python:3.9

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

RUN FLASK_ENV=production

CMD ["python", "app/app.py"]