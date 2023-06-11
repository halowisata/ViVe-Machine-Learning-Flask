FROM python:3.9

# Install necessary dependencies
RUN apt-get update && apt-get install -y ...

# Install the compatible version of tensorflow-intel
RUN pip install tensorflow-intel==2.12.0

# Copy your application code
COPY . /app

# Set the working directory
WORKDIR /app

# Install additional requirements, if any
RUN pip install -r requirements.txt

# Set the command to run your application
CMD [ "python", "./app/app.py" ]