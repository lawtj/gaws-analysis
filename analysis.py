import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import streamlit as st

st.set_page_config(layout="wide")
pd.options.plotting.backend = "plotly"
pio.templates.default = 'seaborn'

df = pd.read_csv('analysis.csv')

#Group for individual country analysis
dfg = df.groupby('country').mean()
dfg = dfg.reset_index()
provnumbers = dfg[['country', 'totalpap','totalpap_cap', 'totalnpap','totalnpap_cap', 'totalproviders', 'totalproviders_cap']].round(0)

#Group by World Bank income group
wbc = df.groupby('wbincome').mean()
wbc = wbc.reset_index()

#Group by WHO Regional group
who = df.groupby('Region').mean()
who = who.reset_index()

###########################################
############## begin layout
###########################################

st.title('GAWS analysis')

st.subheader('# of providers per 100,00 people (per capita)')

###########################################
col1, col2 = st.columns(2)
with col1:
    st.write('#### number of providers by World Bank Income Group')
    fig = px.bar(wbc, x='wbincome', y=['totalpap_cap', 'totalnpap_cap'], barmode='group')
    fig.update_xaxes(categoryorder='total descending')
    st.plotly_chart(fig)

with col2:
    st.write('#### providers by WHO Group')
    fig = px.bar(who, x='Region', y=['totalpap_cap', 'totalnpap_cap'], barmode='group')
    fig.update_xaxes(categoryorder='total descending')
    st.plotly_chart(fig)

###########################################
st.write('### Table of absolute and per capita provider numbers')
st.dataframe(provnumbers)

###########################################
st.subheader('% of providers that are women')

col1, col2 = st.columns(2)
with col1:
    st.write('#### % providers who are women, by World Bank Income Group')
    fig = px.bar(wbc, x='wbincome', y=['totalpap_gender', 'totalnpap_gender'], barmode='group')
    fig.update_xaxes(categoryorder='total descending')
    st.plotly_chart(fig)

with col2:
    st.write('#### % providers who are women, by WHO Group')
    fig = px.bar(who, x='Region', y=['totalpap_gender', 'totalnpap_gender'], barmode='group')
    fig.update_xaxes(categoryorder='total descending')
    st.plotly_chart(fig)
    st.caption('Blue = Physicians, Orange = nonphysicisans')

###########################################
