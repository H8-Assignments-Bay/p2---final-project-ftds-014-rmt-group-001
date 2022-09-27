import streamlit as st
import Page_1
import Page_2
import Page_3

st.set_page_config(
    page_title="StockGuruu",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="expanded",
   )

PAGES = {
    "Fundamental Analysis": Page_1,
    "Technical Analysis": Page_2,
    "Sentimental Analysis": Page_3
}


st.sidebar.title("Section")
selection = st.sidebar.selectbox("Choose Pages", list(PAGES.keys())
)


st.title("StockGuruu App")

page = PAGES[selection]
page.app()