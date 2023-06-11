FROM python:3.9

# Copy your application code
COPY . /app

# Set the working directory
WORKDIR /app

# Set the command to run your application
CMD [ "python", "./app/app.py" ]