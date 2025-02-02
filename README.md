# Sales Dashboard Streamlit

## Overview

This project is a sales performance dashboard built using Streamlit. It allows users to visualize and analyze sales data stored in a PostgreSQL database. The dashboard provides key metrics, visualizations, and raw data to help understand sales performance over time.

## Features

- **Interactive Dashboard**: User-friendly interface to explore sales data.
- **Key Metrics**: Displays total revenue, total orders, average order value, and top category.
- **Dynamic Visualizations**:
  - **Revenue Over Time**: Line chart showing revenue trends.
  - **Revenue by Category**: Bar chart displaying revenue distribution across categories.
  - **Top Products**: Pie chart highlighting top-selling products.
- **Data Filtering**: Filter data by date range, category, and product.
- **Raw Data View**: Table view to explore the raw sales data.
- **CSV Export**: Export filtered data to CSV for further analysis.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/sales-dashboard-streamlit.git
    cd sales-dashboard-streamlit
    ```

2. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up PostgreSQL database**:
    - Ensure PostgreSQL is installed and running on your machine.
    - Create a database named `sales_db`.
    - Update the `DB_CONFIG` dictionary in [generate_data.py](http://_vscodecontentref_/1) and [app.py](http://_vscodecontentref_/2) with your PostgreSQL credentials if they differ.

4. **Generate and insert data**:
    ```sh
    python generate_data.py
    ```

## Usage

1. **Run the Streamlit app**:
    ```sh
    streamlit run app.py
    ```

2. **Open your browser** and navigate to `http://localhost:8501` to view the dashboard.

## File Structure

- [generate_data.py](http://_vscodecontentref_/3): Script to generate and insert sales data into the PostgreSQL database.
- [app.py](http://_vscodecontentref_/4): Streamlit application to visualize and analyze sales data.
- [requirements.txt](http://_vscodecontentref_/5): List of required Python packages.
- [generated_data.csv](http://_vscodecontentref_/6): CSV file containing the generated sales data.
- [README.md](http://_vscodecontentref_/7): Project documentation.

## Dependencies

- Streamlit
- Pandas
- Matplotlib
- Psycopg2-binary
- Polars
- Numpy

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Psycopg2](https://www.psycopg.org/)
- [Polars](https://www.pola.rs/)
- [Numpy](https://numpy.org/)



