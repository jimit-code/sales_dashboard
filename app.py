import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='	📊 Sales Performance Dashboard"', layout = 'wide')

@st.cache_data
def load_data():
    df = pd.read_csv('superstore.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['ship_date'] = pd.to_datetime(df['ship_date'])
    df['Month'] = df['order_date'].dt.to_period('M').astype(str)
    df['ship_days'] = (df['ship_date'] - df['order_date']).dt.days
    return df

df = load_data()

st.sidebar.header('Filter Data')

region = st.sidebar.multiselect("Select Region", df['region'].unique())
category = st.sidebar.multiselect('Select Category', df['category'].unique())

filtered_df = df.copy()

if region:
    filtered_df = filtered_df[filtered_df['region'].isin(region)]
if category:
    filtered_df = filtered_df[filtered_df['category'].isin(category)]

st.markdown("### :chart_with_upwards_trend: Key Performance Matrics")

total_sales = filtered_df['sales'].sum()
avg_u_orders = filtered_df['order_id'].nunique()
avg_order_value = round(total_sales / avg_u_orders, 2) if avg_u_orders else 0
total_quantity = filtered_df['quantity'].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(':dart: Total Sales', round(total_sales, 2))
with col2:
    st.metric(':page_with_curl: Unique Orders', avg_u_orders)
with col3:
    st.metric(':money_with_wings: Avg. Order Value', avg_order_value)
with col4:
    st.metric(':pencil: Quantity Ordered', total_quantity)

st.markdown("### 📈 Sales by Sub-Category")

subcat = filtered_df.groupby('subcategory', as_index=False)['sales'].sum().sort_values(by='sales', ascending=False)
fig_bar = px.bar(
    subcat,
    x = 'subcategory',
    y = 'sales',
    title = 'Top Performing Sub-Categories',
    text_auto='.2s',
    template = 'seaborn'
)
st.plotly_chart(fig_bar)

st.markdown("## 🔍 State-wise Sales and ")

col5, col6 = st.columns(2)

with col5:
    state = filtered_df.groupby('state', as_index=False)['sales'].sum().sort_values(by = 'sales', ascending = False)
    fig_state = px.bar(
        state,
        x = 'state',
        y = 'sales',
        labels={'state': 'States',
                'Sales' :'Satewise Sales'},
        template= 'seaborn'

    )
    st.plotly_chart(fig_state)

with col6:
   segment = filtered_df.groupby('segment', as_index=False)['sales'].sum().sort_values(by = 'sales', ascending = False)
   fig_segment = px.pie(
       segment,
       values= 'sales',
       names = 'segment',
       hole = 0.4,
       template='plotly'
   )
   st.plotly_chart(fig_segment)

col8, col9 = st.columns(2)

with col8:
    st.markdown("### Shipping Time Per Region")
    ship_days = filtered_df.groupby('category', as_index=False)['ship_days'].mean()
    fig_shipdays = px.pie(
        ship_days,
        values= 'ship_days',
        names= 'category',
        hole= 0.4
    )
    st.plotly_chart(fig_shipdays)

with col9:
    monthly_sales = (
        filtered_df
        .groupby('Month', as_index=False)['sales']
        .sum()
        .sort_values(by='Month')  # ⬅️ sort by time, not by sales!
    )

    fig_monthly = px.line(
        monthly_sales,
        x='Month',
        y='sales',
        title='Monthly Sales Trend',
        template='plotly_dark',
        markers=True,  # optional: show points
        labels={'sales': 'Total Sales', 'Month': 'Month'}
    )

    st.plotly_chart(fig_monthly, use_container_width=True)
