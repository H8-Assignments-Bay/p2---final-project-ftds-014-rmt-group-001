import streamlit as st
from datetime import date
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from alpha_vantage.fundamentaldata import FundamentalData 


def app():
    st.subheader('Technical Analysis')
    API_key = 'ZFX92CIREXMQRIZV'

    ts = TimeSeries(key = API_key, output_format = 'pandas')
    ticker = st.text_input("Enter the Stock Code of company","AAPL")
    st.subheader('Company Profile',ticker)

    @st.cache(allow_output_mutation=True)
    def load_daily(ticker):
        data_day = ts.get_intraday(ticker)
        data_day = data_day[0]
        return data_day

    @st.cache(allow_output_mutation=True)
    def load_data(ticker): 
        data = ts.get_weekly(ticker)
        data = data[0]
        return data
    data = load_data(ticker)

    data_day = load_daily(ticker) 

    eodPrices   = pd.DataFrame(data=data['4. close'])
    percentageChange = eodPrices.pct_change()
    data['Percentage'] = percentageChange


    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    st.subheader(ticker)


    st.subheader('Stock Chart')
    st.line_chart(data['1. open']) 

    st.subheader('Stock Intraday Chart')
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Candlestick(x=data_day.index,
                                open=data_day['1. open'],
                                high=data_day['2. high'],
                                low=data_day['3. low'],
                                close=data_day['4. close'],
                                ))

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
    )

    st.plotly_chart(fig)