import streamlit as st
from datetime import date
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from alpha_vantage.fundamentaldata import FundamentalData 


def app():
    st.subheader('Fundamental Analysis')
    API_key = 'ZFX92CIREXMQRIZV'
    fd = FundamentalData(key = API_key, output_format = 'pandas', indexing_type = 'date')
    ticker = st.text_input("Enter the Stock Code of company","AAPL")
    st.subheader(ticker)
    st.subheader('Company Profile',ticker)

    data_fund, meta_data = fd.get_company_overview(symbol = ticker)

    string_summary = data_fund['Description'].to_list()
    st.info(string_summary)

    companyInfo = {
            "Country": data_fund['Country'],
            "Address": data_fund['Address'],
            "Sector": data_fund['Sector'],
            "Industry": data_fund['Industry'],
            'Exchange': data_fund['Exchange'],
        }

    compDF = pd.DataFrame.from_dict(companyInfo, orient='index')
    compDF = compDF.rename(columns={0: 'Value'})
    st.table(compDF)    


    fundInfo = {
            "Market Cap": data_fund["MarketCapitalization"],
            "PBV Ratio": data_fund['PriceToBookRatio'],
            "PE Ratio": data_fund['PERatio'],
            "PEG Ratio": data_fund['PEGRatio'],
            'Book Value': data_fund['BookValue'],
            'Earnings per Share': data_fund['EPS'],
            "Profit Margin": data_fund['ProfitMargin'],
            'Dividend Yield': data_fund['DividendYield'],
            "Beta": data_fund['Beta'],
            '52 Week High': data_fund['52WeekHigh'],
            '52 Week Low': data_fund['52WeekLow']
        }

    fundDF = pd.DataFrame.from_dict(fundInfo, orient='index')
    fundDF = fundDF.rename(columns={0: 'Value'})

    st.subheader('Fundamental Info') 
    st.table(fundDF)


