# # Use an official Python runtime as a parent image
# FROM python:3.9

# # Set the working directory inside the container
# WORKDIR /alpha-vantage-data-pipeline

# # Copy the requirements file
# COPY requirements.txt .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the etl directory and other necessary files
# COPY . .

# # Command to run your Python script
# CMD ["python", "etl/currency_exchange_etl.py"]

FROM apache/airflow:2.5.1-python3.9

USER root

# Install PostgreSQL development libraries and GCC
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN mkdir -p /opt/airflow/logs && chmod -R 777 /opt/airflow/logs

USER airflow

# Install dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt