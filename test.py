# Imports
import streamlit as st
import pandas as pd
import numpy as np
import calendar
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pio.templates.default = "plotly"

# This has to be at the top of the script always
st.set_page_config(layout="wide")
st.title(":bank: Failed Banks Analysis")

# Renderinf the
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


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


def banks_failed_year(year):
    df_year = df[df["faildate"].dt.strftime("%Y") == str(year)]
    return df_year


st.sidebar.header("Dashboard `v1.0.0`")


get_Selection = st.sidebar.radio(
    "Make selection based on your choices", ["Year", "State"]
)


failed = 10
st.markdown("### Metrics")
col1, col2, col3, col4 = st.columns(4)

if get_Selection == "Year":
    fail_year = st.sidebar.selectbox("**Select Year**", df["faildate"].dt.year.unique())
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
else:
    fail_year = "2023"

if get_Selection == "State":
    get_state = st.sidebar.selectbox("**Select State**", df["state"].unique())
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
else:
    get_state = "CA"


st.write("#")
st.write("#")
st.write("#")


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
tab1, tab2 = st.tabs(["Year", "States"])

with tab1:
    st.header("Plot for Year Wise Failures")
    st.plotly_chart(
        get_fig_plot1(x, y1, y2), theme="streamlit", use_container_width=True
    )

with tab2:
    st.header("Plot for Failures in the given State from 2000-2023")
    st.plotly_chart(
        plot2(states_failed_df), theme="streamlit", use_container_width=True
    )

st.sidebar.markdown(
    """
---
Created with ❤️ by [Soham](https://sohambhagwat.tech).
"""
)
