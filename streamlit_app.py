import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout='wide')
st.title('🎈 Failed Banks Analysis')


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


@st.cache_data
def get_data(csv1, csv2):

    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2,encoding='windows-1252')
    df1.columns = df1.columns.str.lower()
    df2.columns = df2.columns.str.lower()
    df2.columns = df2.columns.str.rstrip()
    df = pd.merge(df1 , df2, on = 'cert')
    columns = ['fin','id','city','closing date','fund','bank name','cityst']
    df = df.drop(columns, axis=1)
    df = df.fillna(0)
    return df

df = get_data('bank-data.csv','banklist.csv')
df['faildate'] = pd.to_datetime(df['faildate'])

def banks_failed_year(year):
    df_year = df[df['faildate'].dt.strftime('%Y') == str(year)]
    return df_year


st.sidebar.header('Dashboard `v1.0.0`')



get_Selection = st.sidebar.radio("Make selection based on your choices",
                 ['Year', 'State'])   






failed = 10
st.markdown('### Metrics')
col1, col2, col3, col4 = st.columns(4)

if get_Selection == 'Year':
    fail_year = st.sidebar.selectbox('**Select Year**', df['faildate'].dt.year.unique())
    col1.metric("Banks failed in {}".format(str(fail_year)), str(len(banks_failed_year(fail_year))), "1.2 °F")
    col2.metric("Estimated Loss", "$"+str(banks_failed_year(fail_year)['cost'].sum()))
    col3.metric("Total Deposits", "$"+str(banks_failed_year(fail_year)['qbfdep'].sum()))
    col4.metric("Total Assets",'$'+str(banks_failed_year(fail_year)['qbfasset'].sum()))

elif get_Selection == 'State':
    get_state = st.sidebar.selectbox('**Select State**',df['state'].unique())
    print(type(get_state))
    col1.metric("Banks failed in {}".format(get_state), len(df[df['state'] == get_state]), "1.2 °F")
    col2.metric("Estimated Loss", "$"+str(df[df['state'] == get_state]['cost'].sum()))
    col3.metric("Total Deposits", "$" + str(df[df['state'] == get_state]['qbfdep'].sum()))
    col4.metric("Total Assets",'$'+str(df[df['state'] == get_state]['qbfasset'].sum()))



st.sidebar.markdown('''
---
Created with ❤️ by [Soham](https://sohambhagwat.tech).
''')
