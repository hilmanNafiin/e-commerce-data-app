import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from func1 import DataAnalyzer, BrazilMapPlotter
from babel.numbers import format_currency
sns.set(style='dark')

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("all_data.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

# Geolocation Dataset
geolocation = pd.read_csv('geolocation.csv')
data = geolocation.drop_duplicates(subset='customer_unique_id')

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    st.title("Tugas Pengantar Sains Data")
    st.image("anggota.png")
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]

function = DataAnalyzer(main_df)
map_plot = BrazilMapPlotter(data, plt, mpimg, urllib, st)

daily_orders_df = function.create_daily_orders_df()
sum_spend_df = function.create_sum_spend_df()
sum_order_items_df = function.create_sum_order_items_df()
review_score, common_score = function.review_score_df()
state, most_common_state = function.create_bystate_df()
order_status, common_status = function.create_order_status()
monthly_orders_df = function.create_monthly_orders_df()
monthly_spend_df = function.create_monthly_spend_df()
bycity_df = function.create_bycity_df()
review_distribution = function.create_review_distribution_df()

# Title
st.header("E-Commerce Dashboard :convenience_store:")

# Order Items
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_df["product_count"].sum()
    st.markdown(f"Total Items: **{total_items}**")

with col2:
    avg_items = sum_order_items_df["product_count"].mean()
    st.markdown(f"Average Items: **{avg_items:.2f}**")

# Grafik Produk Paling Banyak dan Paling Sedikit Terjual
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 12))

# Warna untuk grafik
colors_top = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
colors_bottom = ["#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

# Grafik Produk Paling Banyak Terjual
sns.barplot(
    x="product_count", 
    y="product_category_name_english", 
    data=sum_order_items_df.head(5), 
    palette=colors_top, 
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=20)
ax[0].set_title("Produk Paling Banyak Terjual", loc="center", fontsize=20)
ax[0].tick_params(axis='y', labelsize=15)
ax[0].tick_params(axis='x', labelsize=15)

# Grafik Produk Paling Sedikit Terjual
sns.barplot(
    x="product_count", 
    y="product_category_name_english", 
    data=sum_order_items_df.sort_values(by="product_count", ascending=True).head(5), 
    palette=colors_bottom, 
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=20)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk Paling Sedikit Terjual", loc="center", fontsize=20)
ax[1].tick_params(axis='y', labelsize=15)
ax[1].tick_params(axis='x', labelsize=15)
st.pyplot(fig)

with st.expander("See Explanation"):
        st.write('Terlihat pada grafik diatas, Produk yang paling banya terjual adalah bed_bath_table. dan produk yang paling sedikit terjual adalah auto.')

# Monthly Spend Money
st.subheader("Monthly Spend Money")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    monthly_spend_df["order_approved_at"],
    monthly_spend_df["total_spend"],
    marker="o",
    linewidth=2,
    color="#33FF57"
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
ax.set_title("Total Spend per Month", fontsize=20)
ax.set_xlabel("Month", fontsize=15)
ax.set_ylabel("Total Spend", fontsize=15)
st.pyplot(fig)

with st.expander("See Explanation"):
        st.write('Pada grafik diatas, total uang yang dihabiskan paling banyak pada bilang November dan paling sedikit pada bulan September.')
        
# Monthly Orders
st.subheader("Monthly Orders")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    monthly_orders_df["order_approved_at"],
    monthly_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#FF5733"
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
ax.set_title("Number of Orders per Month", fontsize=20)
ax.set_xlabel("Month", fontsize=15)
ax.set_ylabel("Number of Orders", fontsize=15)
st.pyplot(fig)

with st.expander("See Explanation"):
        st.write('Terlihat pada grafik diatas bahwa terjadi penurunan signifikan pada bulan September dan mengalami penaikan yang signifikan pada bulan November. Chart pada Monthly Order mengalami trend yang sama seperti pada Monthly Spend.')

# Review Score Distribution
st.subheader("Review Score Distribution")
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    review_distribution.values,
    labels=review_distribution.index,
    autopct='%1.1f%%',
    colors=sns.color_palette("viridis", len(review_distribution))
)
ax.set_title("Distribution of Review Scores", fontsize=20)
st.pyplot(fig)

with st.expander("See Explanation"):
        st.write('Pie Chart menunjukan bahwa review didominasi oleh score 5 sebanyak 56.2 persen dan total score kurang dari sama dengan 3 sebanyak 24.9 persen. Ini berarti customer menunjukan respon positif')

# Order Status
st.subheader("Order Status")
common_status_ = order_status.value_counts().index[0]
st.markdown(f"Most Common Order Status: **{common_status_}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x=order_status.index,
    y=order_status.values,
    palette="plasma",
    ax=ax
)
ax.set_title("Order Status Distribution", fontsize=20)
ax.set_xlabel("Status", fontsize=15)
ax.set_ylabel("Count", fontsize=15)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

with st.expander("See Explanation"):
        st.write('Grafik menunjukan bahwa terdapat 115723 produk yang dalam status delivered dan status lain kurang dari 1300 produk')

# Customer Demographic
st.subheader("Customer Demographic")
tab1, tab2, tab3 = st.tabs(["State", "City", "Geolocation"])

with tab1:
    most_common_state = state.customer_state.value_counts().index[0]
    st.markdown(f"Most Common State: **{most_common_state}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x=state.customer_state.value_counts().index,
        y=state.customer_count.values, 
        palette="viridis",
        ax=ax
    )
    ax.set_title("Number of Customers from State", fontsize=20)
    ax.set_xlabel("State", fontsize=15)
    ax.set_ylabel("Number of Customers", fontsize=15)
    ax.tick_params(axis='x', labelsize=12)
    st.pyplot(fig)
    
    with st.expander("See Explanation"):
        st.write('Pada grafik diatas berdasarkan State, Saul Paulo memiliki data customer terbanyak. Dengan lima customer terbanyak berdasarkan city, yaitu: \nSao Paulo sebanyak 41746 customers,\nRio De Janeiro sebanyak 12852 customers,\nMinas Gerais sebanyak 11635 customers,\nRio Grande de Sul sebanyak 5466 customers,\nParana sebanyak 5045 customers.')

with tab2:
    st.subheader("Top 10 Cities by Number of Customers")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x=bycity_df["customer_count"].head(10),
        y=bycity_df["customer_city"].head(10),
        palette="magma",
        ax=ax
    )
    ax.set_title("Top 10 Cities by Number of Customers", fontsize=20)
    ax.set_xlabel("Number of Customers", fontsize=15)
    ax.set_ylabel("City", fontsize=15)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    st.pyplot(fig)
    
    with st.expander("See Explanation"):
        st.write('Pada grafik diatas berdasarkan State, Saul Paulo memiliki data customer terbanyak. Dengan lima customer terbanyak berdasarkan city, yaitu: \nSao Paulo sebanyak 18875 customers,\nRio De Janeiro sebanyak 8311 customers,\nBelo Horizonte sebanyak 3299 customers,\nBrasilia sebanyak 2500 customers,\nCuritiba sebanyak 1827 customers.')


with tab3:
    map_plot.plot()

    with st.expander("See Explanation"):
        st.write('Sesuai dengan grafik yang sudah dibuat, ada lebih banyak pelanggan di bagian tenggara dan selatan. Informasi lainnya, ada lebih banyak pelanggan di kota-kota yang merupakan ibu kota (São Paulo, Rio de Janeiro, Porto Alegre, dan lainnya).')
