

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as stg  # 🎈 data web app development
import json
import re

stg.set_page_config(
    page_title="ESG Data Dashboard",
    page_icon="✅",
    layout="wide",
)


# read csv from a github repo
dataset_url = 'data.csv'

img = 'test2.png'

# read csv from a URL
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

data_base = get_data()


data_base["industry"].fillna("No industry", inplace = True)
data_base["logo"].fillna("No logo", inplace = True)
data_base["weburl"].fillna("No url", inplace = True)
data_base.isnull().sum()

# dashboard title
stg.title("ESG Data Dashboard")

list_type = ['Total Score', 'Environment Score', 'Social Score', 'Governance Score']


# top-level filters

        # create three columns
stg.markdown('### Grade Range')
stg.image(img, use_column_width=True)
name_filter = stg.selectbox("Select the Name", pd.unique(data_base["name"]))

score_filter = stg.selectbox("Select the Score", list_type)

# creating a single-element container
placeholder = stg.empty()


# dataframe filter

if score_filter == 'Environment Score':
    score_type= 'environment_score'
if score_filter == 'Total Score':
    score_type= 'total_score'
if score_filter == 'Governance Score':
    score_type= 'governance_score'
if score_filter == 'Social Score':
    score_type= 'social_score'

df = data_base[data_base["name"] == name_filter]


data_name_ind_1 = str(df["industry"]).split(' ',1)[1]
data_name_ind = data_name_ind_1.split('\n')[0].strip()

df_ind = data_base[data_base["industry"] == data_name_ind]


 # creating KPIs
avg_score = np.mean(df["total_score"])
avg_score_ind = np.mean(df_ind["total_score"])
total_grade = str(df['total_grade']).split(' ',1)[1]
total_grade = total_grade.split('\n')[0].strip()

environment = np.mean(df["environment_score"])
environment_ind = np.mean(df_ind["environment_score"])
env_grade = str(df['environment_grade']).split(' ',1)[1]
env_grade = total_grade.split('\n')[0].strip()

social = np.mean(df["social_score"])
social_ind = np.mean(df_ind["social_score"])
social_grade = str(df['social_grade']).split(' ',1)[1]
social_grade = total_grade.split('\n')[0].strip()

governance = np.mean(df["governance_score"])
governance_ind = np.mean(df_ind["governance_score"])
gov_grade = str(df['governance_grade']).split(' ',1)[1]
gov_grade = total_grade.split('\n')[0].strip()

data_name_str = str(df['name']).split(' ',1)[1]
data_name = data_name_str.split('\n')[0].strip()

data_base['category'] = np.where(data_base['industry'] == data_name_ind , '1', '0')

data_base['cat2'] = np.where(data_base['name'] == data_name , '1', '0')

data_base['Rank'] = data_base[score_type].rank(ascending = False)

rank = data_base.loc[data_base['name'] == data_name, 'Rank']
rank = str(rank).split('\n')

max_val = str(data_base['Rank'].max()).split('.')[0]


with placeholder.container():

    grades = str(data_base['total_grade'].unique())

    stg.markdown('## Company Data: ' + data_name)
    stg.markdown('### Industry: ' + data_name_ind)


           # create two columns for charts
    fig_col1,  = stg.columns(1)
    with fig_col1:
        stg.markdown("### Company Performance: " + score_filter)
        stg.markdown('### Rank: ' + rank[0][3:].split('.')[0] + '/' + max_val) 
        fig = px.histogram(
            data_frame=data_base,  labels={
                     score_type: "Score",
                     "name": "Company",
                 }, y=score_type, x="name", color='cat2', color_discrete_map= {'0': "#b9cbec",
                                      '1': "#EF0107"}, height = 700)
        fig.update_layout(xaxis_title=None, barmode='stack', xaxis={'categoryorder':'total descending'}, showlegend=False, font_size = 5)
        fig.update_xaxes(showticklabels=False)
        stg.write(fig)

    stg.markdown('### Grades & Scores')
    kpi1, kpi2, kpi3, kpi4 = stg.columns(4)

        # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="Total Grade",
        value=total_grade,
    )
        
    kpi2.metric(
        label="Environmental Grade",
        value=env_grade

     )
        
    kpi3.metric(
        label="Social Grade",
        value=social_grade

        )
    kpi4.metric(
        label="Governance Grade",
        value=gov_grade
        )
    

    kpi1, kpi2, kpi3, kpi4 = stg.columns(4)

        # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="Total Score",
        value=int(avg_score),
        delta = int(avg_score)- int(avg_score_ind)
    )
        
    kpi2.metric(
        label="Environmental Score",
        value=int(environment),
        delta = int(environment)- int(environment_ind)

     )
        
    kpi3.metric(
        label="Social Score",
        value=int(social),
        delta = int(social) - int(social_ind)

        )
    kpi4.metric(
        label="Governance Score",
        value=int(governance),
        delta = int(governance) - int(governance_ind)
        )

    kpi1, kpi2, kpi3, kpi4 = stg.columns(4)

        # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="Industry Total Score",
        value=int(avg_score_ind),
    )
        
    kpi2.metric(
        label="Industry Environmental Score",
        value=int(environment_ind),

     )
        
    kpi3.metric(
        label=" Industry Social Score",
        value=int(social_ind),

        )
    kpi4.metric(
        label="Industry Governance Score",
        value=int(governance_ind),
        )




        # create two columns for charts
    color = {data_name:'#2c7bb6'}
    fig_col1, = stg.columns(1)
    with fig_col1:
        stg.markdown("### Industry Ranking: " + score_filter)
        fig = px.histogram(
            data_frame=data_base,  labels={
                     score_type: "Score",
                     "industry": "Industry",
                 }, y=score_type, x="industry", color='category', color_discrete_map= {'0': "#b9cbec",
                                      '1': "#EF0107"}, height = 700)
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}, showlegend=False, font_size = 5)

        stg.write(fig)

   
            
            

    stg.markdown("### Detailed Data View")
    stg.dataframe(df)
