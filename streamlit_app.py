import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV
@st.cache_data
def load_data():
    return pd.read_csv("generated_data.csv")

df = load_data()

def get_date_range():
    return pd.to_datetime(df['order_date']).min(), pd.to_datetime(df['order_date']).max()

def get_unique_categories():
    return df['categories'].unique().tolist()

def get_dashboard_stats(start_date, end_date, category):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df[(pd.to_datetime(df['order_date']) >= start_date) & (pd.to_datetime(df['order_date']) <= end_date)]
    if category != 'All Categories':
        filtered_df = filtered_df[filtered_df['categories'] == category]
    total_revenue = filtered_df['total'].sum()
    total_orders = filtered_df['customer_id'].nunique()  # Updated column name
    avg_order_value = total_revenue / total_orders if total_orders else 0
    top_category = filtered_df.groupby('categories')['total'].sum().idxmax() if not filtered_df.empty else "N/A"
    return total_revenue, total_orders, avg_order_value, top_category

def get_plot_data(start_date, end_date, category):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df[(pd.to_datetime(df['order_date']) >= start_date) & (pd.to_datetime(df['order_date']) <= end_date)]
    if category != 'All Categories':
        filtered_df = filtered_df[filtered_df['categories'] == category]
    return filtered_df.groupby('order_date')['total'].sum().reset_index()

def get_revenue_by_category(start_date, end_date, category):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df[(pd.to_datetime(df['order_date']) >= start_date) & (pd.to_datetime(df['order_date']) <= end_date)]
    if category != 'All Categories':
        filtered_df = filtered_df[filtered_df['categories'] == category]
    return filtered_df.groupby('categories')['total'].sum().reset_index()

def get_top_products(start_date, end_date, category):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df[(pd.to_datetime(df['order_date']) >= start_date) & (pd.to_datetime(df['order_date']) <= end_date)]
    if category != 'All Categories':
        filtered_df = filtered_df[filtered_df['categories'] == category]
    return filtered_df.groupby('product_names')['total'].sum().reset_index().nlargest(10, 'total')

def get_raw_data(start_date, end_date, category):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df[(pd.to_datetime(df['order_date']) >= start_date) & (pd.to_datetime(df['order_date']) <= end_date)]
    if category != 'All Categories':
        filtered_df = filtered_df[filtered_df['categories'] == category]
    return filtered_df

def plot_data(data, x_col, y_col, title, xlabel, ylabel, orientation='v'):
    fig, ax = plt.subplots(figsize=(10, 6))
    if not data.empty:
        if orientation == 'v':
            ax.bar(data[x_col], data[y_col])
        else:
            ax.barh(data[x_col], data[y_col])
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.xticks(rotation=45)
    else:
        ax.text(0.5, 0.5, "No data available", ha='center', va='center')
    return fig

# Streamlit App
st.title("Sales Performance Dashboard")

# Filters
with st.container():
    col1, col2, col3 = st.columns([1, 1, 2])
    min_date, max_date = get_date_range()
    start_date = col1.date_input("Start Date", min_date.date())
    end_date = col2.date_input("End Date", max_date.date())
    categories = get_unique_categories()
    category = col3.selectbox("Category", ["All Categories"] + categories)

# Custom CSS for metrics
st.markdown("""
    <style>
    .metric-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .metric-container {
        flex: 1;
        padding: 10px;
        text-align: center;
        background-color: #f0f2f6;
        border-radius: 5px;
        margin: 0 5px;
    }
    .metric-label {
        font-size: 14px;
        color: #555;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 18px;
        font-weight: bold;
        color: #0e1117;
    }
    </style>
""", unsafe_allow_html=True)

# Metrics
st.header("Key Metrics")
stats = get_dashboard_stats(start_date, end_date, category)
if stats:
    total_revenue, total_orders, avg_order_value, top_category = stats
else:
    total_revenue, total_orders, avg_order_value, top_category = 0, 0, 0, "N/A"

# Custom metrics display
metrics_html = f"""
<div class="metric-row">
    <div class="metric-container">
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">${total_revenue:,.2f}</div>
    </div>
    <div class="metric-container">
        <div class="metric-label">Total Orders</div>
        <div class="metric-value">{total_orders:,}</div>
    </div>
    <div class="metric-container">
        <div class="metric-label">Average Order Value</div>
        <div class="metric-value">${avg_order_value:,.2f}</div>
    </div>
    <div class="metric-container">
        <div class="metric-label">Top Category</div>
        <div class="metric-value">{top_category}</div>
    </div>
</div>
"""
st.markdown(metrics_html, unsafe_allow_html=True)

# Visualization Tabs
st.header("Visualizations")
tabs = st.tabs(["Revenue Over Time", "Revenue by Category", "Top Products"])

# Revenue Over Time Tab
with tabs[0]:
    st.subheader("Revenue Over Time")
    revenue_data = get_plot_data(start_date, end_date, category)
    st.pyplot(plot_data(revenue_data, 'order_date', 'total', "Revenue Over Time", "Date", "Revenue"))

# Revenue by Category Tab
with tabs[1]:
    st.subheader("Revenue by Category")
    category_data = get_revenue_by_category(start_date, end_date, category)
    st.pyplot(plot_data(category_data, 'categories', 'total', "Revenue by Category", "Category", "Revenue"))

# Top Products Tab
with tabs[2]:
    st.subheader("Top Products")
    top_products_data = get_top_products(start_date, end_date, category)
    st.pyplot(plot_data(top_products_data, 'product_names', 'total', "Top Products", "Revenue", "Product Name", orientation='h'))

st.header("Raw Data")

raw_data = get_raw_data(
    start_date=start_date,
    end_date=end_date,
    category=category
)

# Removed the index by resetting it and dropping the old index
raw_data = raw_data.reset_index(drop=True)

st.dataframe(raw_data, hide_index=True)

st.write("")