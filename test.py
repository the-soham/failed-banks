import streamlit as st
import pandas as pd
import numpy as np
import calendar
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pio.templates.default = "plotly"
  #plotly graph object-data visualization
import streamlit as st                #GUI
from streamlit_option_menu import option_menu   #option menu
import time



st.set_page_config(
     page_title="Failed Banks data visualization",
     layout="wide",
     initial_sidebar_state="expanded",)

@st.cache_data
def get_data(csv1, csv2):
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2, encoding="windows-1252")
    df1.columns = df1.columns.str.lower()
    df2.columns = df2.columns.str.lower()
    df2.columns = df2.columns.str.rstrip()
    df = pd.merge(df1, df2, on="cert")
    columns = ["fin", "id", "city", "closing date", "fund", "bank name", "cityst"]
    df = df.drop(columns, axis=1)
    df = df.fillna(0)
    return df


df = get_data("bank-data.csv", "banklist.csv")
df["faildate"] = pd.to_datetime(df["faildate"])
df["year"] = df["faildate"].dt.year
df["month"] = df["faildate"].dt.month
df["Month_Year"] = df["faildate"].dt.to_period("M")
df['Day'] = df['faildate'].apply(lambda time: time.dayofweek)
df['Day'] = df['Day'].map({
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
})


def banks_failed_year(year):
    df_year = df[df["faildate"].dt.strftime("%Y") == str(year)]
    return df_year


def plot1(df):
    df_overall = df.groupby('year')['year'].count().reset_index(name = 'counts')
    fig = px.line(df_overall, x="year", y="counts", title='Banks failures from 2000 - 2023',text="year")
    fig.update_traces(textposition="bottom right")
    return fig

def plot_day(df):
    from calendar import day_name
    df_day = df.groupby('Day')['Day'].count().reset_index(name = 'counts')
    idx=(df_day['Day'].map({v:k for k,v in dict(enumerate(calendar.day_name)).items()})
        .sort_values().index)
    df_day = df_day.reindex(idx)
    fig = px.bar(df_day, x = 'Day', y = 'counts')
    return fig

def plot_month(df):
    df_month  = df.groupby('month')['month'].count().reset_index(name='counts')
    df_month['month'] = df_month['month'].apply(lambda x: calendar.month_abbr[x])
    fig = px.bar(df_month, x='month', y='counts')
    return fig


st.title(":bank: Failed Banks Analysis")
# Hide the streamlit app content
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)


with st.sidebar:
    main = option_menu(None, ["Home", 'Visualization'],icons=['house', 'pin-map'], menu_icon="cast")

with st.sidebar:
    with st.spinner("Loading..."):
        time.sleep(1)


###----

if main == 'Home':

    st.markdown("#### Welcome to the data visualization regarding the bank failures in the States! ")
    st.markdown('Bank failures are relatively common and there are numerous reasons behind these failure ranging from the bank\'s business model to the  lack of stringent regulations ')
    st.markdown('But the back-to-back collapses of Silicon Valley Bank (SVB) and Signature Bank—followed by the failure of First Republic Bank just seven weeks later triggered a wave of concern amongst the general public.')
    st.markdown('In this analysis we delve deeper into [FDIC\'s](https://www.fdic.gov/analysis/) database to gain insights into the bank failures in the United States since the year 2000.')
    st.markdown("Click on the ****:red[Visualization]**** option in the sidebar to start exploring the [FDIC\'s](https://www.fdic.gov/) data.")
    st.write('The dataset for this project can be found [here](https://www.fdic.gov/analysis/) and the code can be found [here](https://github.com/the-soham/failed-banks).' )
    st.write ('For any collaboration regarding Data science / ML projects, I can be reached via my [email](sohambhagwat2@gmail.com).Checkout my [portfolio](https://sohambhagwat.tech)')
    st.write('#')
    st.write('#')
    st.markdown('Created with ❤️ by [Soham](https://sohambhagwat.tech).')

if main== "Visualization":
    
    st.markdown('### How common are the Bank Failure\'s?')
    st.plotly_chart(plot1(df), theme="streamlit", use_container_width=True)


    with st.expander("See Analysis"):
        st.write(
                """
                 From the plot we can see that the bank failures are common, but they've become rare in recent years. 
                 During the Great Recession we can see that over hundereds of banks failed.
                  Although since the year 2015 we can see that the very few banks have failed. """
                 )
    st.markdown('#')
    st.markdown('---')
    st.markdown('#')
    st.markdown('### On what day\'s do the bank failures happen the most')
    st.plotly_chart(plot_day(df), theme="streamlit", use_container_width=True)
    with st.expander("See Analysis"):
        st.write(
                """
                 From the plot we can see that the bank rarely fail on the weekends.
                Signature Bank, which [failed](https://www.fdic.gov/resources/resolutions/bank-failures/failed-bank-list/signature-ny.html) on Sunday, March 13, 2023, is an exception. 
                Traditionally, banks operate Monday through Friday and close on weekends. If the FDIC waits to take over a failing bank until Friday, it has the entire weekend to settle accounts, 
                liquidate assets and transition to new management before customers start demanding their money.
                The need to oversee a smooth transition and keep panic contained isn’t just about one bank’s customers.
                If regulators don’t do a good job of cushioning the fall when a bank collapses, customers at other banks could start worrying they’ll lose their money, prompting bank runs all over the country. 
                This self-fulfilling prophecy can trigger a financial crisis.
                [Reference](https://www.forbes.com/advisor/banking/list-of-failed-banks/)"""
                 )
    
    st.markdown('#')
    st.markdown('---')
    st.markdown('#')
    st.markdown('### In which month have the banks failed the most?')
    st.plotly_chart(plot_month(df), theme="streamlit", use_container_width=True)
    with st.expander("See Analysis"):
        st.write(
                """
                 From the plot, we can observe that most of the bank failures occur at the start of the new quarter."""
                 )
    
