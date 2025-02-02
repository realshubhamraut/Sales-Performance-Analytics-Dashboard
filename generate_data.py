import polars as pl
import numpy as np
from datetime import datetime, timedelta
import psycopg2

# PostgreSQL connection details
DB_CONFIG = {
    "dbname": "sales_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

def generate_data(nrows: int):
    names = np.array([
        "Laptop", "Smartphone", "Desk", "Chair", "Monitor",
        "Printer", "Paper", "Pen", "Notebook", "Coffee Maker",
        "Cabinet", "Plastic Cups"
    ])

    categories = np.array([
        "Electronics", "Electronics", "Office", "Office",
        "Electronics", "Electronics", "Stationery", "Stationery",
        "Stationery", "Electronics", "Office", "Sundry"
    ])

    product_id = np.random.randint(len(names), size=nrows)
    quantity = np.random.randint(1, 11, size=nrows)
    price = np.random.randint(199, 10000, size=nrows) / 100

    start_date = datetime(2010, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = (end_date - start_date).days
    order_dates = np.array([(start_date + timedelta(days=np.random.randint(0, date_range))).strftime('%Y-%m-%d') for _ in range(nrows)])

    columns = {
        "order_date": order_dates,
        "customer_id": np.random.randint(100, 1000, size=nrows),
        "customer_name": [f"Customer_{i}" for i in np.random.randint(2**15, size=nrows)],
        "product_id": product_id + 200,
        "product_names": names[product_id],
        "categories": categories[product_id],
        "quantity": quantity,
        "price": price,
        "total": price * quantity,
    }

    df = pl.DataFrame(columns)
    df.write_csv("/Users/proxim/PROXIM/PROJECTS/Sales-Dashboard-Streamlit/generated_data.csv")
    return df

def insert_data_to_db(df):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        for row in df.iter_rows():
            cur.execute("""
                INSERT INTO sales_data (order_date, customer_id, customer_name, product_id, product_names, categories, quantity, price, total)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(row))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

# Generate and insert 100,000 records
df = generate_data(100000)
insert_data_to_db(df)