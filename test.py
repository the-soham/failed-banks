import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout='wide')
st.title('🎈 Failed Banks Analysis')


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


df1 = pd.read_csv('bank-data.csv')
df2 = pd.read_csv('banklist.csv',encoding='windows-1252')
df1.columns = df1.columns.str.lower()
df2.columns = df2.columns.str.lower()
df2.columns = df2.columns.str.rstrip()
df = pd.merge(df1 , df2, on = 'cert')
columns = ['fin','id','city','closing date','fund','bank name','cityst']
df = df.drop(columns, axis=1)
df = df.fillna(0)
df['faildate'] = pd.to_datetime(df['faildate'])



st.sidebar.header('Dashboard `v1.0.0`')



get_Selection = st.sidebar.radio("Make selection based on your choices",
                 ['Year', 'State'])   

if get_Selection == 'Year':
    time_hist_color = st.sidebar.selectbox('**Select Year**', df['faildate'].dt.year.unique())
elif get_Selection == 'State':
    get_state = st.sidebar.selectbox('**Select State**',df['state'].unique())

st.sidebar.markdown('''
---
Created with ❤️ by [Soham](https:sohambhagwat.tech).
''')

st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")