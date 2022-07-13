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
dfg = df.groupby(['country','Region']).mean()
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

st.subheader('1. # of providers per 100,00 people (per capita)')

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
st.write('#### Raw data of absolute and per capita provider numbers')
st.dataframe(provnumbers)

###########################################
st.subheader('2. % of providers that are women')

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
########### comparison to previous GAWS

st.header('Comparison to previous GAWS')
st.write('This compares the current GAWS per capita numbers vs the GAWS per capita numbers in 2015. A number greater than 1 indicates increase by x% (eg. 1.5 is a 1.5x increase, or 150%). A number less than 1 indicates a decrease. ')

dfg=dfg.sort_values(by='physiciancap_diff')

######europe
st.write('#### European Region')
col1, col2 = st.columns(2)
with col1:
    fig = px.bar(x=dfg[dfg['Region']=='European Region']['country'], y=dfg[dfg['Region']=='European Region']['physiciancap_diff'])
    st.plotly_chart(fig)

with col2:
    dfg[dfg['Region']=='European Region'][['country', 'totalpap_cap', 'physicians2015', 'physiciancap_diff']]

#########africa
st.write('#### African Region')
col1, col2 = st.columns(2)
with col1:
    fig = px.bar(x=dfg[dfg['Region']=='African Region']['country'], y=dfg[dfg['Region']=='African Region']['physiciancap_diff'])
    st.plotly_chart(fig)
    st.caption('Tanzania is a clear outlier, with almost 26x growth since 2015?')

with col2:
    dfg[dfg['Region']=='African Region'][['country', 'totalpap_cap', 'physicians2015', 'physiciancap_diff']]

############ americas
st.write('#### Americas Region')
col1, col2 = st.columns(2)
with col1:
    fig = px.bar(x=dfg[dfg['Region']=='Region of the Americas']['country'], y=dfg[dfg['Region']=='Region of the Americas']['physiciancap_diff'])
    st.plotly_chart(fig)

with col2:
    dfg[dfg['Region']=='Region of the Americas'][['country', 'totalpap_cap', 'physicians2015', 'physiciancap_diff']]

########## EMRO
st.write('#### Eastern Mediterranean Region')
col1, col2 = st.columns(2)
with col1:
    fig = px.bar(x=dfg[dfg['Region']=='Eastern Mediterranean Region']['country'], y=dfg[dfg['Region']=='Eastern Mediterranean Region']['physiciancap_diff'])
    st.plotly_chart(fig)

with col2:
    st.dataframe(dfg[dfg['Region']=='Eastern Mediterranean Region'][['country', 'totalpap_cap', 'physicians2015', 'physiciancap_diff']])

########## SEASIA
st.write('#### South-East Asia Region')
col1, col2 = st.columns(2)
with col1:
    fig = px.bar(x=dfg[dfg['Region']=='South-East Asia Region']['country'], y=dfg[dfg['Region']=='South-East Asia Region']['physiciancap_diff'])
    st.plotly_chart(fig)

with col2:
    st.dataframe(dfg[dfg['Region']=='South-East Asia Region'][['country', 'totalpap_cap', 'physicians2015', 'physiciancap_diff']])

st.write('#### Western Pacific Region')
col1, col2 = st.columns(2)
with col1:
    fig = px.bar(x=dfg[dfg['Region']=='Western Pacific Region']['country'], y=dfg[dfg['Region']=='Western Pacific Region']['physiciancap_diff'])
    st.plotly_chart(fig)

with col2:
    st.dataframe(dfg[dfg['Region']=='Western Pacific Region'][['country', 'totalpap_cap', 'physicians2015', 'physiciancap_diff']])