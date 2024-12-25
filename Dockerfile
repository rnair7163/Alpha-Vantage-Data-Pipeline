# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /alpha-vantage-data-pipeline

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the etl directory and other necessary files
COPY . .

# Command to run your Python script
CMD ["python", "etl/currency_exchange_etl.py"]