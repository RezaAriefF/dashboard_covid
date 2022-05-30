import streamlit as st
import pandas as pd
import plotly.express as px
from turtle import width
import numpy as np
from PIL import Image
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tugas dari kelompok 8",
	page_icon=":bar_chart:",
	layout="wide")

st.title("Dashboard Penjualan")
st.write("Menampilkan data penjualan dari negara tetangga")
image = Image.open("log1.png")
st.image(image, width=500)
st.markdown("Dengan anggota kelompok 8")
st.markdown("1.Annisa Nurul Kazhimah")
st.markdown("2.Aulia Salsabila Haning Puspita")
st.markdown("3.Muhammad Ranzha Nicola")
st.markdown("4.Rafly Electrica Nurillah")
st.markdown("5.Reza Arief Firmanda")

@st.cache
def get_data_from_excel():
	df = pd.read_excel(
		io='data.xlsx',
		engine='openpyxl',
		sheet_name='Sales',
		skiprows=3,
		usecols='B:R',
		nrows=1000,

	)

	df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
	return df

df = get_data_from_excel()


#st.dataframe(df)

st.sidebar.header("Filter data :")
city = st.sidebar.multiselect(
    "Pilih berdasarkan kota:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Berdasarkan level pelanggan:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Berdasarkan jenis kelamin:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
	"City == @city & Customer_type == @customer_type & Gender == @gender"
)

st.dataframe(df_selection)
st.title(":bar_chart: Dashboard Penjualan")
st.markdown("##")

total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, midle_column, right_column = st.columns(3)
with left_column:
	st.subheader("Total Penjualan:")
	st.subheader(f"US $ {total_sales:,}")
with midle_column:
	st.subheader("Rata - Rata Rating")
	st.subheader(f"{average_rating} {star_rating}")
with right_column:
	st.subheader("Rata - rata penjualan per-transaksi:")
	st.subheader(f"US $ {average_sale_by_transaction}",
)

st.markdown("---")

sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_produk_sales = px.bar(
	sales_by_product_line,
	x="Total",
	y=sales_by_product_line.index,
	orientation="h",
	title="<b>Penjualan produk dengan visualisasi diagram batang</b>",
	color_discrete_sequence=["#40E0D0"] * len(sales_by_product_line),
	template="plotly_white",
)
fig_produk_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    )
st.plotly_chart(fig_produk_sales)

sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Penjualan per jam</b>",
    color_discrete_sequence=["#66CDAA"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_hourly_sales)
