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


    with st.expander("See Analysis", expanded = True):
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
    with st.expander("See Analysis",expanded=True):
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
    with st.expander("See Analysis",expanded=True):
        st.write(
                """
                 From the plot, we can observe that most of the bank failures occur at the start of the new quarter."""
                 )
    
    st.markdown('#')
    st.markdown('---')
    st.markdown('#')
    st.markdown('### In which  have the banks failed the most?')
    st.plotly_chart(plot_month(df), theme="streamlit", use_container_width=True)
    with st.expander("See Analysis",expanded=True):
        st.write(
                """
                 From the plot, we can observe that most of the bank failures occur at the start of the new quarter."""
                 )
        

    st.markdown('#')
    st.markdown('---')
    st.markdown('#')

    sel = st.radio(
        "**Make the choice about Year/State**",
        ('Year', 'State'), horizontal=True)
       
    if sel == 'Year':
        fail_year = st.selectbox("**Select Year**", df["faildate"].dt.year.unique())
    else:
        fail_year ='2023'

    if sel == 'State':
        get_state = st.selectbox("**Select State**", df["state"].unique())
    else:
        get_state = 'AL'

    def get_year_loss(df, fail_year):
        yr = df[df["faildate"].dt.strftime("%Y") == str(fail_year)]

        df_yr = yr.groupby(["year", "month"])["month"].count().reset_index(name="counts")
        df_yr = df_yr.set_index("month")
        df_yr = df_yr.reindex(np.arange(1, 13)).fillna(0.0)
        df_yr["year"] = fail_year
        df_yr = df_yr.reset_index()

        df_cost = yr.groupby(["year", "month"])["cost"].sum().reset_index(name="loss")
        df_cost = df_cost.set_index("month")
        df_cost = df_cost.reindex(np.arange(1, 13)).fillna(0.0)
        df_cost["year"] = fail_year
        df_cost = df_cost.reset_index()

        df_final = pd.merge(df_yr, df_cost)
        df_final["month"] = df_final["month"].apply(lambda x: calendar.month_abbr[x])

        return df_final


    def get_year_state(df, get_state):
        st = df[df["state"] == str(get_state)]
        df_st = st.groupby(["year", "state"])["year"].count().reset_index(name="count")
        df_st = df_st.set_index("year")
        df_st = df_st.reindex(np.arange(2000, 2024)).fillna(0.0)
        df_st["state"] = str(get_state)
        df_st = df_st.reset_index()
        return df_st


    states_failed_df = get_year_state(df, get_state)


    def get_fig_plot1(x, y1, y2, yr=fail_year):
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scatter(x=x, y=y1, name="Loss ", line_color="#ffe476"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=x, y=y2, name="Bank Failures", line=dict(color="#0000ff")),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(title_text="Loss and Bank Failures in {}".format(yr))

        # Set x-axis title
        fig.update_xaxes(title_text="Months ")

        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Total loss ($m)</b>", secondary_y=False)
        fig.update_yaxes(title_text="<b>Number ofBanks Failed </b>", secondary_y=True)

        fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

        return fig


    def plot2(df, st_name=str(get_state)):
        fig = px.line(
            df, x="year", y="count", title="Banks failed in the state of {} from 2000-2023".format(st_name)
        )
        return fig


    final_df = get_year_loss(df, fail_year)
    x = final_df["month"]
    y1 = final_df["loss"]
    y2 = final_df["counts"]
            
      

    st.markdown("### Metrics")
    col1, col2, col3, col4 = st.columns(4)

    if sel == "Year":
        
        col1.metric(
            "Banks failed in {}".format(str(fail_year)),
            str(len(banks_failed_year(fail_year))),
        )
        col2.metric(
            "Estimated Loss", "$" + str(banks_failed_year(fail_year)["cost"].sum()) + "M"
        )
        col3.metric(
            "Total Deposits", "$" + str(banks_failed_year(fail_year)["qbfdep"].sum()) + "M"
        )
        col4.metric(
            "Total Assets", "$" + str(banks_failed_year(fail_year)["qbfasset"].sum()) + "M"
        )

        st.markdown('#')

        st.markdown("### Plot for Year Wise Failures")
        st.plotly_chart(
            get_fig_plot1(x, y1, y2), theme="streamlit", use_container_width=True
        )
    if sel == "State":

        col1.metric(
            "Banks failed in {}".format(get_state),
            len(df[df["state"] == get_state]),
        )
        col2.metric(
            "Estimated Loss", "$" + str(df[df["state"] == get_state]["cost"].sum()) + "M"
        )
        col3.metric(
            "Total Deposits", "$" + str(df[df["state"] == get_state]["qbfdep"].sum()) + "M"
        )
        col4.metric(
            "Total Assets", "$" + str(df[df["state"] == get_state]["qbfasset"].sum()) + "M"
        )

        st.markdown('#')
        st.markdown("### Plot for Failures in the given State from 2000-2023")
        st.plotly_chart(
            plot2(states_failed_df), theme="streamlit", use_container_width=True
        )




