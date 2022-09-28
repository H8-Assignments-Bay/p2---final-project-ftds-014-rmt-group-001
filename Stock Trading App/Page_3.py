# Web Scraping tools
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import plotly.express as px
import pandas as pd
import streamlit as st
# VADER for Sentiment Analysis
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def app():
    # for extracting data from finviz
    finviz_url = 'https://finviz.com/quote.ashx?t='
    ticker = st.text_input("Enter the Stock Code of company","AAPL")
    st.subheader(ticker + ' News Sentiment Analysis')

    def get_news(ticker):
        url = finviz_url + ticker
        # Act as a browser
        req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}) 
        response = urlopen(req)    
        # Read the contents of the file into 'html'
        html = BeautifulSoup(response)
        # Find the id through inspect element and find news table
        news_table = html.find(id='news-table')
        return news_table
    
    news_table = get_news(ticker)

    # parse news into dataframe
    def parse_news(news_table):
        parsed_news = []

        for x in news_table.findAll('tr'):
            # read the text from each tr tag into text
            # get text from a only
            text = x.a.get_text() 
            # splite text in the td tag into a list 
            date_scrape = x.td.text.split()
            # if the length of 'date_scrape' is 1, load 'time' as the only element

            if len(date_scrape) == 1:
                time = date_scrape[0]

            # else load 'date' as the 1st element and 'time' as the second    
            else:
                date = date_scrape[0]
                time = date_scrape[1]

            # Append ticker, date, time and headline as a list to the 'parsed_news' list
            parsed_news.append([date, time, text])        
            # Set column names
            columns = ['date', 'time', 'headline']
            # Convert the parsed_news list into a DataFrame called 'parsed_and_scored_news'
            parsed_news_df = pd.DataFrame(parsed_news, columns=columns)        
            # Create a pandas datetime object from the strings in 'date' and 'time' column
            parsed_news_df['datetime'] = pd.to_datetime(parsed_news_df['date'] + ' ' + parsed_news_df['time'])

        return parsed_news_df

    parsed_news_df = parse_news(news_table)

    # Instantiate the sentiment intensity analyzer
    new_words = {
    'crushes': 10,
    'beats': 5,
    'misses': -5,
    'trouble': -10,
    'falls': -100,
    'drop': -10,
    'crash': -10,
    'bearish': -10,
    'bear': -5}
    vader = SentimentIntensityAnalyzer()
    vader.lexicon.update(new_words)

    def score_news(parsed_news_df):

        # Iterate through the headlines and get the polarity scores using vader
        scores = parsed_news_df['headline'].apply(vader.polarity_scores).tolist()
        # Convert the 'scores' list of dicts into a DataFrame
        scores_df = pd.DataFrame(scores)

        # Join the DataFrames of the news and the list of dicts
        parsed_and_scored_news = parsed_news_df.join(scores_df)        
        parsed_and_scored_news = parsed_and_scored_news.set_index('datetime')    
        parsed_and_scored_news = parsed_and_scored_news.drop(['date', 'time'],axis= 1)          
        parsed_and_scored_news = parsed_and_scored_news.rename(columns={"compound": "sentiment_score"})

        return parsed_and_scored_news

    parsed_and_scored_news = score_news(parsed_news_df)
    
    def plot_daily_sentiment(parsed_and_scored_news, ticker):

        # Group by date and ticker columns from scored_news and calculate the mean
        mean_scores = parsed_and_scored_news.resample('D').mean()

        # Plot a bar chart with plotly 
        fig = px.bar(mean_scores, x=mean_scores.index, y='sentiment_score', title = ticker + ' Daily Sentiment Scores')
        return fig

    def plot_hourly_sentiment(parsed_and_scored_news, ticker):

        # Group by date and ticker columns from scored_news and calculate the mean
        mean_scores = parsed_and_scored_news.resample('H').mean()

        # Plot a bar chart with plotly 
        fig2 = px.bar(mean_scores, x=mean_scores.index, y='sentiment_score', title = ticker + ' Hourly Sentiment Scores')
        return fig2
        

       
    news_table = get_news(ticker)
    parsed_news_df = parse_news(news_table)
    parsed_and_scored_news = score_news(parsed_news_df)
    fig_hourly = plot_hourly_sentiment(parsed_and_scored_news, ticker)
    fig_daily = plot_daily_sentiment(parsed_and_scored_news,ticker)
    st.plotly_chart(fig_hourly)
    st.plotly_chart(fig_daily)

    description = """
    The above chart is the average sentiment scores of {} stock hourly and daily.
    The Table below is the most recent news taken from finviz website.
    Sentiments are given by the nltk.sentiment.vader Python library and adjusted to know terms of stock market.
    """.format(ticker)
                
    st.write(description)	 
    st.table(parsed_and_scored_news).header


