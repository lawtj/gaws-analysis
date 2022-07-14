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
provnumbers = dfg[['country','Region', 'totalpap','totalpap_cap', 'totalnpap','totalnpap_cap', 'totalproviders', 'totalproviders_cap','physicians2015', 'physicians2015_cap', 'physiciancap_diff']]
#provnumbers.to_csv('provider numbers.csv')


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

st.header('1. # of providers per 100,00 people (per capita)')

###########################################
left, right = st.columns(2)

with left:
    st.markdown("""
    There are some significant discrepancies between the old 2015 data and the new ones. These will have to be validated, particularly for extreme changes.

    - Some countries have reported a many-fold increase in providers and providers per capita
    - Some have show a significant decrease

    """
    )

with right:
    st.markdown("""

    **Table legend**
    - Country
    - Region
    - ***totalpap***: total physician providers
    - ***totalpap_cap***: total physician providers per capita
    - ***totalnpap***: total NPAPs
    - ***totalnpap_cap***: total NPAPs per capita
    - ***totalproviders***: sum of total PAP and total NPAP
    - ***totalproviders_cap***: total # of providers (PAP & NPAP) per capita
    - ***physicians2015***: total physician providers from 2015 GAWS
    - ***physicians2015_cap***: total physician providers per capita from 2015 GAWS
    - ***physiciancap_diff***: total physician providers per capita / total physician providers per capita from 2015
    """)

col1, col2 = st.columns(2)
with col1:
    st.write('#### number of providers by World Bank Income Group')
    fig = px.bar(wbc, x='wbincome', y=['totalpap_cap', 'totalnpap_cap'], barmode='group', text_auto=True)
    fig.update_xaxes(categoryorder='total descending')
    st.plotly_chart(fig)

with col2:
    st.write('#### providers by WHO Group')
    fig = px.bar(who, x='Region', y=['totalpap_cap', 'totalnpap_cap'], barmode='group', text_auto=True)
    fig.update_xaxes(categoryorder='total descending')
    st.plotly_chart(fig)

###########################################
st.write('#### Raw data of absolute and per capita provider numbers')
st.dataframe(provnumbers)

###########################################
st.header('2. % of providers that are women')

col1, col2 = st.columns(2)
with col1:
    st.write('#### % providers who are women, by World Bank Income Group')
    fig = px.bar(wbc, x='wbincome', y=['totalpap_gender', 'totalnpap_gender'], barmode='group', text_auto=True)
    fig.update_xaxes(categoryorder='total descending')
    st.plotly_chart(fig)

with col2:
    st.write('#### % providers who are women, by WHO Group')
    fig = px.bar(who, x='Region', y=['totalpap_gender', 'totalnpap_gender'], barmode='group', text_auto=True)
    fig.update_xaxes(categoryorder='total descending')
    st.plotly_chart(fig)
    st.caption('Blue = Physicians, Orange = nonphysicisans')

###########################################
########### comparison to previous GAWS

st.header('3. Comparison of PAPs to previous GAWS')
st.subheader('Raw data to compare, current vs 2015 GAWS')
provnumbers
st.write('This compares the current GAWS per capita numbers vs the GAWS per capita numbers in 2015. A number greater than 1 indicates increase by x% (eg. 1.5 is a 1.5x increase, or 150%). A number less than 1 indicates a decrease. ')

dfg=dfg.sort_values(by='physiciancap_diff')

## use t3 for grouped bar graphs
t3 = dfg[['country', 'Region','totalpap_cap', 'physicians2015_cap']]
t3= t3.melt(id_vars=['Region','country'])

######europe
st.write('#### European Region')


fig = px.bar(x=t3[t3['Region']=='European Region']['country'], y=t3[t3['Region']=='European Region']['value'], color=t3[t3['Region']=='European Region']['variable'], barmode='group', text_auto=True)
fig.update_xaxes(categoryorder='total descending')

st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.write('% difference from last survey')
    fig = px.bar(x=dfg[dfg['Region']=='European Region']['country'], y=dfg[dfg['Region']=='European Region']['physiciancap_diff'], text_auto=True)
    st.plotly_chart(fig)

with col2:
    dfg[dfg['Region']=='European Region'][['country','totalpap', 'totalpap_cap','physicians2015', 'physicians2015_cap', 'physiciancap_diff']]

#########africa
st.write('#### African Region')

fig = px.bar(x=t3[t3['Region']=='African Region']['country'], y=t3[t3['Region']=='African Region']['value'], color=t3[t3['Region']=='African Region']['variable'], barmode='group', text_auto=True)
fig.update_xaxes(categoryorder='total descending')

st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(x=dfg[dfg['Region']=='African Region']['country'], y=dfg[dfg['Region']=='African Region']['physiciancap_diff'], text_auto=True)
    st.plotly_chart(fig)
    st.caption('Tanzania is a clear outlier, with almost 26x growth since 2015?')

with col2:
    dfg[dfg['Region']=='African Region'][['country','totalpap', 'totalpap_cap','physicians2015', 'physicians2015_cap', 'physiciancap_diff']]

############ americas
st.write('#### Americas Region')

fig = px.bar(x=t3[t3['Region']=='Region of the Americas']['country'], y=t3[t3['Region']=='Region of the Americas']['value'], color=t3[t3['Region']=='Region of the Americas']['variable'], barmode='group', text_auto=True)
fig.update_xaxes(categoryorder='total descending')

st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(x=dfg[dfg['Region']=='Region of the Americas']['country'], y=dfg[dfg['Region']=='Region of the Americas']['physiciancap_diff'], text_auto=True)
    st.plotly_chart(fig)

with col2:
    dfg[dfg['Region']=='Region of the Americas'][['country','totalpap', 'totalpap_cap','physicians2015', 'physicians2015_cap', 'physiciancap_diff']]

########## EMRO
st.write('#### Eastern Mediterranean Region')

fig = px.bar(x=t3[t3['Region']=='Eastern Mediterranean Region']['country'], y=t3[t3['Region']=='Eastern Mediterranean Region']['value'], color=t3[t3['Region']=='Eastern Mediterranean Region']['variable'], barmode='group', text_auto=True)
fig.update_xaxes(categoryorder='total descending')

st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(x=dfg[dfg['Region']=='Eastern Mediterranean Region']['country'], y=dfg[dfg['Region']=='Eastern Mediterranean Region']['physiciancap_diff'], text_auto=True)
    st.plotly_chart(fig)

with col2:
    st.dataframe(dfg[dfg['Region']=='Eastern Mediterranean Region'][['country','totalpap', 'totalpap_cap','physicians2015', 'physicians2015_cap', 'physiciancap_diff']])

########## SEASIA
st.write('#### South-East Asia Region')

fig = px.bar(x=t3[t3['Region']=='South-East Asia Region']['country'], y=t3[t3['Region']=='South-East Asia Region']['value'], color=t3[t3['Region']=='South-East Asia Region']['variable'], barmode='group', text_auto=True)
fig.update_xaxes(categoryorder='total descending')

st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(x=dfg[dfg['Region']=='South-East Asia Region']['country'], y=dfg[dfg['Region']=='South-East Asia Region']['physiciancap_diff'], text_auto=True)
    st.plotly_chart(fig)

with col2:
    st.dataframe(dfg[dfg['Region']=='South-East Asia Region'][['country','totalpap', 'totalpap_cap','physicians2015', 'physicians2015_cap', 'physiciancap_diff']])

st.write('#### Western Pacific Region')

fig = px.bar(x=t3[t3['Region']=='Western Pacific Region']['country'], y=t3[t3['Region']=='Western Pacific Region']['value'], color=t3[t3['Region']=='Western Pacific Region']['variable'], barmode='group', text_auto=True)
fig.update_xaxes(categoryorder='total descending')

st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(x=dfg[dfg['Region']=='Western Pacific Region']['country'], y=dfg[dfg['Region']=='Western Pacific Region']['physiciancap_diff'], text_auto=True)
    st.plotly_chart(fig)

with col2:
    st.dataframe(dfg[dfg['Region']=='Western Pacific Region'][['country','totalpap', 'totalpap_cap','physicians2015', 'physicians2015_cap', 'physiciancap_diff']])