FROM python:3.9-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install virtualenv && \
    virtualenv /venv && \
    /venv/bin/pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/venv/bin/python", "app.py"]

CMD ["python", "app.py"]