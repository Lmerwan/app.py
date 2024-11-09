import streamlit as st
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objs as go
import appdirs as ad
import yfinance as yf

# Set up your web app with a wider layout and title
st.set_page_config(layout="wide", page_title="Stock Data Explorer")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6; /* Light gray background */
    }
    .sidebar .sidebar-content {
        background-color: #ffffff; /* White sidebar background */
        padding: 20px;
        border-radius: 10px;
    }
    .reportview-container .main .block-container {
        padding: 20px;
    }
    h1, h2 {
        color: #333333; /* Dark gray heading color */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar with title and input fields
st.sidebar.title("Stock Information")
symbol = st.sidebar.text_input('Enter Stock Symbol:', 'AAPL').upper()
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date:', value=datetime.date(2023, 1, 1))
with col2:
    edate = st.date_input('End Date:', value=datetime.date.today())

# Main content area with title and stock data
st.title(f"Stock Data for {symbol}")

# Fetch stock data
stock = yf.Ticker(symbol)

# Display company information with improved formatting
if stock.info:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Sector:** {stock.info['sector']}")
        st.write(f"**Beta:** {stock.info['beta']:.2f}")
    with col2:
        st.write(f"**Market Cap:** {stock.info['marketCap']:,.0f}")
        st.write(f"**P/E Ratio:** {stock.info['forwardPE']:.2f}")
    with col3:
        st.write(f"**Website:** [{stock.info['website']}]({stock.info['website']})")
else:
    st.error("Failed to fetch company data.")

# Download historical data
data = yf.download(symbol, start=sdate, end=edate)

# Create and display interactive line chart with improved styling
if not data.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    fig.update_layout(
        title=f'{symbol} Closing Prices',
        xaxis_title='Date',
        yaxis_title='Close Price',
        template='plotly_dark',  # Using a dark theme
        xaxis=dict(showgrid=False),  # Removing x-axis grid lines
        yaxis=dict(showgrid=False),  # Removing y-axis grid lines
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Failed to fetch historical data.")
