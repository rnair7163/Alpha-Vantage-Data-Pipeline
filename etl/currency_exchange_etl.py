import requests
import os
from dotenv import load_dotenv
import psycopg2 

load_dotenv()

# Load Environmental Variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
API_KEY = os.getenv("API_KEY")


# url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={api_key}"
# url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=INR&apikey={api_key}"
# url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=INR&apikey={api_key}"
# r = requests.get(url)
# data = r.json()

# print(data['Realtime Currency Exchange Rate']['1. From_Currency Code'])

# print(data['Realtime Currency Exchange Rate']["1. From_Currency Code"],
#         # data['Realtime Currency Exchange Rate']["2. From_Currency Name"],
#         data['Realtime Currency Exchange Rate']["3. To_Currency Code"],
#         data['Realtime Currency Exchange Rate']["4. To_Currency Name"],
#         float(data['Realtime Currency Exchange Rate']["5. Exchange Rate"]),
#         data['Realtime Currency Exchange Rate']["6. Last Refreshed"],
#         data['Realtime Currency Exchange Rate']["7. Time Zone"],
#         float(data['Realtime Currency Exchange Rate']["8. Bid Price"]),
#         float(data['Realtime Currency Exchange Rate']["9. Ask Price"])
#     )

# Function to connect to the PostgreSQL database
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connected to the database successfully!")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    
def setup_database(conn):
    schema_query = """
    CREATE SCHEMA IF NOT EXISTS exchange_data;
    """
    table_query = """
    CREATE TABLE IF NOT EXISTS exchange_data.currency_exchange (
        from_currency_code VARCHAR(10),
        to_currency_code VARCHAR(10),
        exchange_rate NUMERIC,
        last_refreshed TIMESTAMP,
        time_zone VARCHAR(10),
        bid_price NUMERIC,
        ask_price NUMERIC
    );
    """
    with conn.cursor() as cursor:
        cursor.execute(schema_query)
        cursor.execute(table_query)
        conn.commit()
        print("Schema and table ensured.")

# Function to insert data into the table
def insert_data(conn, data):
    query = """
    INSERT INTO exchange_data.currency_exchange (
        from_currency_code,
        to_currency_code,
        exchange_rate,
        last_refreshed,
        time_zone,
        bid_price,
        ask_price
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['Realtime Currency Exchange Rate']["1. From_Currency Code"],
        data['Realtime Currency Exchange Rate']["3. To_Currency Code"],
        float(data['Realtime Currency Exchange Rate']["5. Exchange Rate"]),
        data['Realtime Currency Exchange Rate']["6. Last Refreshed"],
        data['Realtime Currency Exchange Rate']["7. Time Zone"],
        float(data['Realtime Currency Exchange Rate']["8. Bid Price"]),
        float(data['Realtime Currency Exchange Rate']["9. Ask Price"])
    )
    with conn.cursor() as cursor:
        cursor.execute(query, values)
        conn.commit()
        print("Data inserted successfully!")
    
def main():
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=INR&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    print(data['Realtime Currency Exchange Rate']["1. From_Currency Code"],
        data['Realtime Currency Exchange Rate']["3. To_Currency Code"],
        float(data['Realtime Currency Exchange Rate']["5. Exchange Rate"]),
        data['Realtime Currency Exchange Rate']["6. Last Refreshed"],
        data['Realtime Currency Exchange Rate']["7. Time Zone"],
        float(data['Realtime Currency Exchange Rate']["8. Bid Price"]),
        float(data['Realtime Currency Exchange Rate']["9. Ask Price"])
    )

    conn = connect_to_db()
    if conn:
        try:
            setup_database(conn)
            insert_data(conn, data)
        finally:
            conn.close()

if __name__ == "__main__":
    main()