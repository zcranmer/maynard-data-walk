# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 08:43:07 2024

@author: ACRANMER

# code for Maynard Climate Resilience Data Walk
"""

import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#os.chdir()

st.set_page_config(layout='wide',
                   page_title='Maynard Climate Resilience Data Walk'
                   )

st.title('Maynard Climate Resilience Data Walk')
st.subheader('Welcome! This page offers data on the Town of Maynard for you \
             to explore. Click on each of the titles below to expand the \
             sections. Each section poses questions for you to consider. Please \
             share your thoughts with us by filling out the survey (link tbd).')
             
text_lang = st.radio('Choose your preferred language:',
                     ['English','Georgian','Spanish','Portugese'],
                     key='text_lang')

@st.cache_resource
def load_data():
    census_api_url = 'https://api.census.gov/data/2022/acs/acs5'
    geography = '&for=county%20subdivision:39625&in=state:25%20county:017'
    
    # import data
    income_url = census_api_url+'?get=group(B19001)'+geography
    income_data = pd.read_csv(income_url)
    income_data = income_data.drop(columns=income_data.columns[income_data.columns.str.contains('A')])
    income_data = income_data.drop(columns=['GEO_ID','state','county','county subdivision]','Unnamed: 73'])
    income_data = income_data.rename(columns={'[["B19001_001E"':'Total Households (Inc)',
                                          'B19001_001M':'Total Households (Inc) Margin of Error',
                                          'B19001_002E':'Less than $10,000',
                                          'B19001_002M':'Less than $10,000 Margin of Error',
                                          'B19001_003E':'$10,000 to $14,999',
                                          'B19001_003M':'$10,000 to $14,999 Margin of Error',
                                          'B19001_004E':'$15,000 to $19,999',
                                          'B19001_004M':'$15,000 to $19,999 Margin of Error',
                                          'B19001_005E':'$20,000 to $24,999',
                                          'B19001_005M':'$20,000 to $24,999 Margin of Error',
                                          'B19001_006E':'$25,000 to $29,999',
                                          'B19001_006M':'$25,000 to $29,999 Margin of Error',
                                          'B19001_007E':'$30,000 to $34,999',
                                          'B19001_007M':'$30,000 to $34,999 Margin of Error',
                                          'B19001_008E':'$35,000 to $39,999',
                                          'B19001_008M':'$35,000 to $39,999 Margin of Error',
                                          'B19001_009E':'$40,000 to $44,999',
                                          'B19001_009M':'$40,000 to $44,999 Margin of Error',
                                          'B19001_010E':'$45,000 to $49,999',
                                          'B19001_010M':'$45,000 to $49,999 Margin of Error',
                                          'B19001_011E':'$50,000 to $59,999',
                                          'B19001_011M':'$50,000 to $59,999 Margin of Error',
                                          'B19001_012E':'$60,000 to $74,999',
                                          'B19001_012M':'$60,000 to $74,999 Margin of Error',
                                          'B19001_013E':'$75,000 to $99,999',
                                          'B19001_013M':'$75,000 to $99,999 Margin of Error',
                                          'B19001_014E':'$100,000 to $124,999',
                                          'B19001_014M':'$100,000 to $124,999 Margin of Error',
                                          'B19001_015E':'$125,000 to $149,999',
                                          'B19001_015M':'$125,000 to $149,999 Margin of Error',
                                          'B19001_016E':'$150,000 to $199,999',
                                          'B19001_016M':'$150,000 to $199,999 Margin of Error',
                                          'B19001_017E':'$200,000 or more',
                                          'B19001_017M':'$200,000 or more Margin of Error'
                                          })
    income_data['Total Households (Inc)'] = income_data['Total Households (Inc)'].str[2:-1]
    income_data['Less than $25,000'] = income_data.loc[0,['Less than $10,000','$10,000 to $14,999','$15,000 to $19,999','$20,000 to $24,999']].sum()
    income_data['$25,000 to $49,999'] = income_data.loc[0,['$25,000 to $29,999','$30,000 to $34,999','$35,000 to $39,999','$40,000 to $44,999','$45,000 to $49,999']].sum()
    income_data['$50,000 to $74,999'] = income_data.loc[0,['$50,000 to $59,999','$60,000 to $74,999']].sum()
    income_cols = ['Less than $25,000','$25,000 to $49,999','$50,000 to $74,999','$75,000 to $99,999',
                   '$100,000 to $124,999','$125,000 to $149,999','$150,000 to $199,999','$200,000 or more']
    income_fig = make_subplots(1,1,
                               #subplot_titles=('Number of Households by Income Bracket')
                               )
    income_fig.add_trace(go.Bar(x=income_data[income_cols].columns,
                            y=income_data.loc[0,income_cols],
                            #error_y=income_data.loc[0,income_data.columns[income_data.columns.str.contains('Margin of Error')]],
                            name='Households by Income Bracket'
                            ))
    income_fig.update_layout(title=dict(text='Number of Households by Income Bracket',font=dict(size=28)),
                  yaxis=dict(title=dict(text='# Households',font=dict(size=18)),
                             tickfont=dict(size=14))
                  )
    income_fig.update_xaxes(tickfont=dict(size=14))
    income_fig.update_layout(hovermode='x',showlegend=False)
    
    med_income_url = census_api_url+'?get=group(B19013)'+geography
    med_inc_data = pd.read_csv(med_income_url)
    med_inc_data = med_inc_data.drop(columns=med_inc_data.columns[med_inc_data.columns.str.contains('A')])
    med_inc_data = med_inc_data.rename(columns={'[["B19013_001E"':'Median Household Income',
                                                'B19013_001M':'MHI Margin of Error'})
    med_inc_data['Median Household Income'] = med_inc_data['Median Household Income'].str[2:-1].astype('int')
    med_inc_data = med_inc_data.drop(columns=['GEO_ID','state','county','county subdivision]','Unnamed: 9'])
    
    med_income_hh_url = census_api_url+'?get=group(B19019)'+geography
    med_inc_hh_data = pd.read_csv(med_income_hh_url)
    med_inc_hh_data = med_inc_hh_data.drop(columns=med_inc_hh_data.columns[med_inc_hh_data.columns.str.contains('A')])
    med_inc_hh_data = med_inc_hh_data.rename(columns={'[["B19019_001E"':'Median Household Income by Household Size',
                                                      'B19019_001M':'MHI by Household Size Margin of Error',
                                                      'B19019_002E':'1-person households',
                                                      'B19019_002M':'1-person households Margin of Error',
                                                      'B19019_003E':'2-person households',
                                                      'B19019_003M':'2-person households Margin of Error',
                                                      'B19019_004E':'3-person households',
                                                      'B19019_004M':'3-person households Margin of Error',
                                                      'B19019_005E':'4-person households',
                                                      'B19019_005M':'4-person households Margin of Error',
                                                      'B19019_006E':'5-person households',
                                                      'B19019_006M':'5-person households Margin of Error',
                                                      'B19019_007E':'6-person households',
                                                      'B19019_007M':'6-person households Margin of Error',
                                                      'B19019_008E':'7-or-more-person households',
                                                      'B19019_008M':'7-or-more-person households'
                                                      })
    med_inc_hh_data['Median Household Income by Household Size'] = med_inc_hh_data['Median Household Income by Household Size'].str[2:-1].astype('int')
    med_inc_hh_data = med_inc_hh_data.drop(columns=['GEO_ID','state','county','county subdivision]','Unnamed: 37'])
    
    #S0101
    age_url = census_api_url+'/subject?get=group(S0101)'+geography
    age_data = pd.read_csv(age_url)
    age_data = age_data.drop(columns=age_data.columns[age_data.columns.str.contains('A')])
    age_data = age_data.drop(columns=['[["GEO_ID"','state','county','county subdivision]','Unnamed: 917'])
    age_data = age_data.rename(columns={'S0101_C01_001E':'Total Population',
                                        'S0101_C01_001M':'Total Population Margin of Error',
                                        'S0101_C01_002E':'Under 5 years',
                                        'S0101_C01_002M':'Under 5 years Margin of Error',
                                        'S0101_C01_003E':'5 to 9 years',
                                        'S0101_C01_003M':'5 to 9 years Margin of Error',
                                        'S0101_C01_004E':'10 to 14 years',
                                        'S0101_C01_004M':'10 to 14 years Margin of Error',
                                        'S0101_C01_005E':'15 to 19 years',
                                        'S0101_C01_005M':'15 to 19 years Margin of Error',
                                        'S0101_C01_006E':'20 to 24 years',
                                        'S0101_C01_006M':'20 to 24 years Margin of Error',
                                        'S0101_C01_007E':'25 to 29 years',
                                        'S0101_C01_007M':'25 to 29 years Margin of Error',
                                        'S0101_C01_008E':'30 to 34 years',
                                        'S0101_C01_008M':'30 to 34 years Margin of Error',
                                        'S0101_C01_009E':'35 to 39 years',
                                        'S0101_C01_009M':'35 to 39 years Margin of Error',
                                        'S0101_C01_010E':'40 to 44 years',
                                        'S0101_C01_010M':'40 to 44 years Margin of Error',
                                        'S0101_C01_011E':'45 to 49 years',
                                        'S0101_C01_011M':'45 to 49 years Margin of Error',
                                        'S0101_C01_012E':'50 to 54 years',
                                        'S0101_C01_012M':'50 to 54 years Margin of Error',
                                        'S0101_C01_013E':'55 to 59 years',
                                        'S0101_C01_013M':'55 to 59 years Margin of Error',
                                        'S0101_C01_014E':'60 to 64 years',
                                        'S0101_C01_014M':'60 to 64 years Margin of Error',
                                        'S0101_C01_015E':'65 to 69 years',
                                        'S0101_C01_015M':'65 to 69 years Margin of Error',
                                        'S0101_C01_016E':'70 to 74 years',
                                        'S0101_C01_016M':'70 to 74 years Margin of Error',
                                        'S0101_C01_017E':'75 to 79 years',
                                        'S0101_C01_017M':'75 to 79 years Margin of Error',
                                        'S0101_C01_018E':'80 to 84 years',
                                        'S0101_C01_018M':'80 to 84 years Margin of Error',
                                        'S0101_C01_019E':'85 years and over',
                                        'S0101_C01_019M':'85 years and over Margin of Error',
                                        'S0101_C01_020E':'5 to 14 years',
                                        'S0101_C01_020M':'5 to 14 years Margin of Error',
                                        'S0101_C01_021E':'15 to 17 years',
                                        'S0101_C01_021M':'15 to 17 years Margin of Error',
                                        'S0101_C01_022E':'Under 18 years',
                                        'S0101_C01_022M':'Under 18 years Margin of Error',
                                        'S0101_C01_023E':'18 to 24 years',
                                        'S0101_C01_023M':'18 to 24 years Margin of Error',
                                        'S0101_C01_024E':'15 to 44 years',
                                        'S0101_C01_024M':'15 to 44 years Margin of Error',
                                        'S0101_C01_025E':'16 years and over',
                                        'S0101_C01_025M':'16 years and over Margin of Error',
                                        'S0101_C01_026E':'18 years and over',
                                        'S0101_C01_026M':'18 years and over Margin of Error',
                                        'S0101_C01_027E':'21 years and over',
                                        'S0101_C01_027M':'21 years and over Margin of Error',
                                        'S0101_C01_028E':'60 years and over',
                                        'S0101_C01_028M':'60 years and over Margin of Error',
                                        'S0101_C01_029E':'62 years and over',
                                        'S0101_C01_029M':'62 years and over Margin of Error',
                                        'S0101_C01_030E':'65 years and over',
                                        'S0101_C01_030M':'65 years and over Margin of Error',
                                        'S0101_C01_031E':'75 years and over',
                                        'S0101_C01_031M':'75 years and over Margin of Error',
                                        'S0101_C01_032E':'Median age (years)',
                                        'S0101_C01_032M':'Median age (years) Margin of Error',
                                        'S0101_C01_033E':'Sex ratio (males per 100 females)',
                                        'S0101_C01_033M':'Sex ratio (males per 100 females) Margin of Error',
                                        'S0101_C01_034E':'Age dependency ratio',
                                        'S0101_C01_034M':'Age dependency ratio Margin of Error',
                                        'S0101_C01_035E':'Old-age dependency ratio',
                                        'S0101_C01_035M':'Old-age dependency ratio Margin of Error',
                                        'S0101_C01_036E':'Child dependency ratio',
                                        'S0101_C01_036M':'Child dependency ratio Margin of Error'
                                        })
    age_data = age_data.drop(columns=age_data.columns[age_data.columns.str.contains('S0101')])
    age_data['25 to 34 years'] = age_data.loc[0,['25 to 29 years','30 to 34 years']].sum()
    age_data['35 to 44 years'] = age_data.loc[0,['35 to 39 years','40 to 44 years']].sum()
    age_data['45 to 54 years'] = age_data.loc[0,['45 to 49 years','50 to 54 years']].sum()
    age_data['55 to 64 years'] = age_data.loc[0,['55 to 59 years','60 to 64 years']].sum()
    
    age_cols = ['Under 5 years','5 to 14 years','15 to 17 years','18 to 24 years',
                '25 to 34 years','35 to 44 years','45 to 54 years','55 to 64 years',
                '65 years and over']
    
    age_fig = make_subplots(1,1)
    age_fig.add_trace(go.Bar(x=age_data[age_cols].columns,
                            y=age_data.loc[0,age_cols],
                            #error_y=age_data.loc[0,age_data.columns[age_data.columns.str.contains('Margin of Error')]],
                            name='People by Age Bracket'
                            ))
    age_fig.update_layout(title=dict(text='Number of People by Age Bracket',font=dict(size=28)),
                  yaxis=dict(title=dict(text='# People',font=dict(size=18)),
                             tickfont=dict(size=14))
                  )
    age_fig.update_xaxes(tickfont=dict(size=14))
    age_fig.update_layout(hovermode='x',showlegend=False)
    
    #Or S1501
    education_url = census_api_url+'?get=group(B15003)'+geography
    education_data = pd.read_csv(education_url)
    education_data = education_data.drop(columns=education_data.columns[education_data.columns.str.contains('A')])
    education_data = education_data.drop(columns=['GEO_ID','state','county','county subdivision]','Unnamed: 105'])
    education_data = education_data.rename(columns={'[["B15003_001E"':'Total Population 25 Years and Over',
                                                    'B15003_001M':'Total Population 25 Years and Over Margin of Error',
                                                    'B15003_002E':'No schooling completed',
                                                    'B15003_002M':'No schooling completed Margin of Error',
                                                    'B15003_003E':'Nursery school',
                                                    'B15003_003M':'Nursery school Margin of Error',
                                                    'B15003_004E':'Kindergarten',
                                                    'B15003_004M':'Kindergarten Margin of Error',
                                                    'B15003_005E':'1st grade',
                                                    'B15003_005M':'1st grade Margin of Error',
                                                    'B15003_006E':'2nd grade',
                                                    'B15003_006M':'2nd grade Margin of Error',
                                                    'B15003_007E':'3rd grade',
                                                    'B15003_007M':'3rd grade Margin of Error',
                                                    'B15003_008E':'4th grade',
                                                    'B15003_008M':'4th grade Margin of Error',
                                                    'B15003_009E':'5th grade',
                                                    'B15003_009M':'5th grade Margin of Error',
                                                    'B15003_010E':'6th grade',
                                                    'B15003_010M':'6th grade Margin of Error',
                                                    'B15003_011E':'7th grade',
                                                    'B15003_011M':'7th grade Margin of Error',
                                                    'B15003_012E':'8th grade',
                                                    'B15003_012M':'8th grade Margin of Error',
                                                    'B15003_013E':'9th grade',
                                                    'B15003_013M':'9th grade Margin of Error',
                                                    'B15003_014E':'10th grade',
                                                    'B15003_014M':'10th grade Margin of Error',
                                                    'B15003_015E':'11th grade',
                                                    'B15003_015M':'11th grade Margin of Error',
                                                    'B15003_016E':'12th grade, no diploma',
                                                    'B15003_016M':'12th grade, no diploma Margin of Error',
                                                    'B15003_017E':'Regular high school diploma',
                                                    'B15003_017M':'Regular high school diploma Margin of Error',
                                                    'B15003_018E':'GED or alternative credential',
                                                    'B15003_018M':'GED or alternative credential Margin of Error',
                                                    'B15003_019E':'Some college, less than 1 year',
                                                    'B15003_019M':'Some college, less than 1 year Margin of Error',
                                                    'B15003_020E':'Some college, 1 or more years, no degree',
                                                    'B15003_020M':'Some college, 1 or more years, no degree Margin of Error',
                                                    'B15003_021E':"Associate's degree",
                                                    'B15003_021M':"Associate's degree Margin of Error",
                                                    'B15003_022E':"Bachelor's degree",
                                                    'B15003_022M':"Bachelor's degree Margin of Error",
                                                    'B15003_023E':"Master's degree",
                                                    'B15003_023M':"Master's degree Margin of Error",
                                                    'B15003_024E':'Professional school degree',
                                                    'B15003_024M':'Professional school degree Margin of Error',
                                                    'B15003_025E':'Doctorate degree',
                                                    'B15003_025M':'Doctorate degree Margin of Error'
                                                    })
    education_data['Total Population 25 Years and Over'] = education_data['Total Population 25 Years and Over'].str[2:-1].astype('int')
    education_data['No high school diploma'] = education_data.loc[0,['No schooling completed','Nursery school','Kindergarten','1st grade',
                                                                     '2nd grade','3rd grade','4th grade','5th grade','6th grade','7th grade',
                                                                     '8th grade','9th grade','10th grade','11th grade','12th grade, no diploma']].sum()
    education_data['High school diploma'] = education_data.loc[0,['Regular high school diploma','GED or alternative credential']].sum()
    education_data['Some college, no degree'] = education_data.loc[0,['Some college, less than 1 year','Some college, 1 or more years, no degree']].sum()
    education_data['Graduate or Professional degree'] = education_data.loc[0,["Master's degree",'Professional school degree','Doctorate degree']].sum()
    
    edu_cols = ['No high school diploma','High school diploma','Some college, no degree',
                "Associate's degree","Bachelor's degree",'Graduate or Professional degree']
    
    edu_fig = make_subplots(1,1)
    edu_fig.add_trace(go.Bar(x=education_data[edu_cols].columns,
                            y=education_data.loc[0,edu_cols],
                            #error_y=education_data.loc[0,education_data.columns[education_data.columns.str.contains('Margin of Error')]],
                            name='People by Educational Attainment'
                            ))
    edu_fig.update_layout(title=dict(text='Number of People by Educational Attainment',font=dict(size=28)),
                  yaxis=dict(title=dict(text='# People',font=dict(size=18)),
                             tickfont=dict(size=14))
                  )
    edu_fig.update_xaxes(tickfont=dict(size=14))
    edu_fig.update_layout(hovermode='x',showlegend=False)
    
    # S1810 includes race along with disability, summary tables work differently from detailed tables
    disability_url = census_api_url+'/subject?get=group(S1810)'+geography
    disability_data = pd.read_csv(disability_url)
    
    disability_data = disability_data.drop(columns=disability_data.columns[disability_data.columns.str.contains('A')])
    disability_data = disability_data.drop(columns=['[["GEO_ID"','state','county','county subdivision]','Unnamed: 833'])
    disability_data = disability_data.rename(columns={'S1810_C02_001E':'Total civilian noninstitutionalized population with a disability',
                                                      'S1810_C02_001M':'Total civilian noninstitutionalized population with a disability Margin of Error',
                                                      'S1810_C02_019E':'With a hearing difficulty',
                                                      'S1810_C02_019M':'With a hearing difficulty Margin of Error',
                                                      'S1810_C02_029E':'With a vision difficulty',
                                                      'S1810_C02_029M':'With a vision difficulty Margin of Error',
                                                      'S1810_C02_039E':'With a cognitive difficulty',
                                                      'S1810_C02_039M':'With a cognitive difficulty Margin of Error',
                                                      'S1810_C02_047E':'With an ambulatory difficulty',
                                                      'S1810_C02_047M':'With an ambulatory difficulty Margin of Error',
                                                      'S1810_C02_055E':'With a self-care difficulty',
                                                      'S1810_C02_055M':'With a self-care difficulty Margin of Error',
                                                      'S1810_C02_063E':'With an independent living difficulty',
                                                      'S1810_C02_063M':'With an independent living difficulty Margin of Error'
                                                      })
    disability_data = disability_data.drop(columns=disability_data.columns[disability_data.columns.str.contains('S1810')])
    
    disability_cols = ['With a hearing difficulty','With a vision difficulty',
                'With a cognitive difficulty','With an ambulatory difficulty',
                'With a self-care difficulty','With an independent living difficulty']
    
    disab = disability_data[disability_cols].rename(columns={'With a hearing difficulty':'Hearing difficulty',
                                                           'With a vision difficulty':'Vision difficulty',
                                                           'With a cognitive difficulty':'Cognitive difficulty',
                                                           'With an ambulatory difficulty':'Ambulatory difficulty',
                                                           'With a self-care difficulty':'Self-care difficulty',
                                                           'With an independent living difficulty':'Independent living difficulty'})
    
    disability_fig = make_subplots(1,2,specs=[[{'type':'scatter'},{'type':'domain'}]],
                                   subplot_titles=('People by Disability Type','Disability by Percent'))
    disability_fig.add_trace(go.Bar(x=disab.columns,y=disab.loc[0,:]
                                    ),
                             row=1,col=1)
    disability_fig.add_trace(go.Pie(labels=disab.columns,values=disab.loc[0,:]
                                    ),row=1,col=2)
    disability_fig.update_layout(title=dict(text='Types of Disabilities',font=dict(size=28)),
                  yaxis=dict(title=dict(text='# People',font=dict(size=18)),
                             tickfont=dict(size=14))
                  )
    disability_fig.update_xaxes(tickfont=dict(size=14))
    disability_fig.update_layout(hovermode='x',showlegend=False)
    
    
    #B16004
    language_url = census_api_url+'?get=group(B16004)'+geography
    language_data = pd.read_csv(language_url)
    language_data = language_data.drop(columns=language_data.columns[language_data.columns.str.contains('A')])
    language_data = language_data.drop(columns=['GEO_ID','state','county','county subdivision]','Unnamed: 273'])
    language_data = language_data.rename(columns={'[["B16004_001E"':'Total Population 5 Years and Over',
                                                  'B16004_001M':'Total Population 5 Years and Over Margin of Error',
                                                  'B16004_004E':'5 to 17 years: Speak Spanish',
                                                  'B16004_004M':'5 to 17 years: Speak Spanish Margin of Error',
                                                  'B16004_007E':'5 to 17 years: Speak Spanish, Speak English not well',
                                                  'B16004_007M':'5 to 17 years: Speak Spanish, Speak English not well Margin of Error',
                                                  'B16004_008E':'5 to 17 years: Speak Spanish, Speak English not at all',
                                                  'B16004_008M':'5 to 17 years: Speak Spanish, Speak English not at all Margin of Error',
                                                  'B16004_009E':'5 to 17 years: Speak other Indo-European languages',
                                                  'B16004_009M':'5 to 17 years: Speak other Indo-European languages Margin of Error',
                                                  'B16004_012E':'5 to 17 years: Speak other Indo-European languages, Speak English not well',
                                                  'B16004_012M':'5 to 17 years: Speak other Indo-European languages, Speak English not well Margin of Error',
                                                  'B16004_013E':'5 to 17 years: Speak other Indo-European languages, Speak English not at all',
                                                  'B16004_013M':'5 to 17 years: Speak other Indo-European languages, Speak English not at all Margin of Error',
                                                  'B16004_014E':'5 to 17 years: Speak Asian and Pacific Island Languages',
                                                  'B16004_014M':'5 to 17 years: Speak Asian and Pacific Island Languages Margin of Error',
                                                  'B16004_017E':'5 to 17 years: Speak Asian and Pacific Island Languages, Speak English not well',
                                                  'B16004_017M':'5 to 17 years: Speak Asian and Pacific Island Languages, Speak English not well Margin of Error',
                                                  'B16004_018E':'5 to 17 years: Speak Asian and Pacific Island Languages, Speak English not at all',
                                                  'B16004_018M':'5 to 17 years: Speak Asian and Pacific Island Languages, Speak English not at all Margin of Error',
                                                  'B16004_019E':'5 to 17 years: Speak other languages',
                                                  'B16004_019M':'5 to 17 years: Speak other languages Margin of Error',
                                                  'B16004_022E':'5 to 17 years: Speak other languages, Speak English not well',
                                                  'B16004_022M':'5 to 17 years: Speak other languages, Speak English not well Margin of Error',
                                                  'B16004_023E':'5 to 17 years: Speak other languages, Speak English not at all',
                                                  'B16004_023M':'5 to 17 years: Speak other languages, Speak English not at all Margin of Error',
                                                  'B16004_026E':'18 to 64 years: Speak Spanish',
                                                  'B16004_026M':'18 to 64 years: Speak Spanish Margin of Error',
                                                  'B16004_029E':'18 to 64 years: Speak Spanish, Speak English not well',
                                                  'B16004_029M':'18 to 64 years: Speak Spanish, Speak English not well Margin of Error',
                                                  'B16004_030E':'18 to 64 years: Speak Spanish, Speak English not at all',
                                                  'B16004_030M':'18 to 64 years: Speak Spanish, Speak English not at all Margin of Error',
                                                  'B16004_031E':'18 to 64 years: Speak other Indo-European languages',
                                                  'B16004_031M':'18 to 64 years: Speak other Indo-European languages Margin of Error',
                                                  'B16004_034E':'18 to 64 years: Speak other Indo-European languages, Speak English not well',
                                                  'B16004_034M':'18 to 64 years: Speak other Indo-European languages, Speak English not well Margin of Error',
                                                  'B16004_035E':'18 to 64 years: Speak other Indo-European languages, Speak English not at all',
                                                  'B16004_035M':'18 to 64 years: Speak other Indo-European languages, Speak English not at all Margin of Error',
                                                  'B16004_036E':'18 to 64 years: Speak Asian and Pacific Island Languages',
                                                  'B16004_036M':'18 to 64 years: Speak Asian and Pacific Island Languages Margin of Error',
                                                  'B16004_039E':'18 to 64 years: Speak Asian and Pacific Island Languages, Speak English not well',
                                                  'B16004_039M':'18 to 64 years: Speak Asian and Pacific Island Languages, Speak English not well Margin of Error',
                                                  'B16004_040E':'18 to 64 years: Speak Asian and Pacific Island Languages, Speak English not at all',
                                                  'B16004_040M':'18 to 64 years: Speak Asian and Pacific Island Languages, Speak English not at all Margin of Error',
                                                  'B16004_041E':'18 to 64 years: Speak other languages',
                                                  'B16004_041M':'18 to 64 years: Speak other languages Margin of Error',
                                                  'B16004_044E':'18 to 64 years: Speak other languages, Speak English not well',
                                                  'B16004_044M':'18 to 64 years: Speak other languages, Speak English not well Margin of Error',
                                                  'B16004_045E':'18 to 64 years: Speak other languages, Speak English not at all',
                                                  'B16004_045M':'18 to 64 years: Speak other languages, Speak English not at all Margin of Error',
                                                  'B16004_048E':'65 years and over: Speak Spanish',
                                                  'B16004_048M':'65 years and over: Speak Spanish Margin of Error',
                                                  'B16004_051E':'65 years and over: Speak Spanish, Speak English not well',
                                                  'B16004_051M':'65 years and over: Speak Spanish, Speak English not well Margin of Error',
                                                  'B16004_052E':'65 years and over: Speak Spanish, Speak English not at all',
                                                  'B16004_052M':'65 years and over: Speak Spanish, Speak English not at all Margin of Error',
                                                  'B16004_053E':'65 years and over: Speak other Indo-European languages',
                                                  'B16004_053M':'65 years and over: Speak other Indo-European languages Margin of Error',
                                                  'B16004_056E':'65 years and over: Speak other Indo-European languages, Speak English not well',
                                                  'B16004_056M':'65 years and over: Speak other Indo-European languages, Speak English not well Margin of Error',
                                                  'B16004_057E':'65 years and over: Speak other Indo-European languages, Speak English not at all',
                                                  'B16004_057M':'65 years and over: Speak other Indo-European languages, Speak English not at all Margin of Error',
                                                  'B16004_058E':'65 years and over: Speak Asian and Pacific Island Languages',
                                                  'B16004_058M':'65 years and over: Speak Asian and Pacific Island Languages Margin of Error',
                                                  'B16004_061E':'65 years and over: Speak Asian and Pacific Island Languages, Speak English not well',
                                                  'B16004_061M':'65 years and over: Speak Asian and Pacific Island Languages, Speak English not well Margin of Error',
                                                  'B16004_062E':'65 years and over: Speak Asian and Pacific Island Languages, Speak English not at all',
                                                  'B16004_062M':'65 years and over: Speak Asian and Pacific Island Languages, Speak English not at all Margin of Error',
                                                  'B16004_063E':'65 years and over: Speak other languages',
                                                  'B16004_063M':'65 years and over: Speak other languages Margin of Error',
                                                  'B16004_066E':'65 years and over: Speak other languages, Speak English not well',
                                                  'B16004_066M':'65 years and over: Speak other languages, Speak English not well Margin of Error',
                                                  'B16004_067E':'65 years and over: Speak other languages, Speak English not at all',
                                                  'B16004_067M':'65 years and over: Speak other languages, Speak English not at all Margin of Error'
                                                  })
    language_data = language_data.drop(columns=language_data.columns[language_data.columns.str.contains('B16004')])
    language_data['Total Population 5 Years and Over'] = language_data['Total Population 5 Years and Over'].str[2:-1]
    
    language_data['Limited English Proficiency'] = language_data.loc[0,['5 to 17 years: Speak Spanish, Speak English not well',
                                                                        '5 to 17 years: Speak Spanish, Speak English not at all',
                                                                        '5 to 17 years: Speak other Indo-European languages, Speak English not well',
                                                                        '5 to 17 years: Speak other Indo-European languages, Speak English not at all',
                                                                        '5 to 17 years: Speak Asian and Pacific Island Languages, Speak English not well',
                                                                        '5 to 17 years: Speak Asian and Pacific Island Languages, Speak English not at all',
                                                                        '5 to 17 years: Speak other languages, Speak English not well',
                                                                        '5 to 17 years: Speak other languages, Speak English not at all',
                                                                        '18 to 64 years: Speak Spanish, Speak English not well',
                                                                        '18 to 64 years: Speak Spanish, Speak English not at all',
                                                                        '18 to 64 years: Speak other Indo-European languages, Speak English not well',
                                                                        '18 to 64 years: Speak other Indo-European languages, Speak English not at all',
                                                                        '18 to 64 years: Speak Asian and Pacific Island Languages, Speak English not well',
                                                                        '18 to 64 years: Speak Asian and Pacific Island Languages, Speak English not at all',
                                                                        '18 to 64 years: Speak other languages, Speak English not well',
                                                                        '18 to 64 years: Speak other languages, Speak English not at all',
                                                                        '65 years and over: Speak Spanish, Speak English not well',
                                                                        '65 years and over: Speak Spanish, Speak English not at all',
                                                                        '65 years and over: Speak other Indo-European languages, Speak English not well',
                                                                        '65 years and over: Speak other Indo-European languages, Speak English not at all',
                                                                        '65 years and over: Speak Asian and Pacific Island Languages, Speak English not well',
                                                                        '65 years and over: Speak Asian and Pacific Island Languages, Speak English not at all',
                                                                        '65 years and over: Speak other languages, Speak English not well',
                                                                        '65 years and over: Speak other languages, Speak English not at all',
                                                                        ]].sum()
    
    language_cols = ['Limited English Proficiency']
    
    language_fig = make_subplots(1,2)
    language_fig.add_trace(go.Bar(x=language_data[language_cols].columns,
                            y=language_data.loc[0,language_cols],
                            #error_y=disability_data.loc[0,disability_data.columns[disability_data.columns.str.contains('Margin of Error')]],
                            name='People with Limited English Proficiency'
                            ))
    language_fig.update_layout(title=dict(text='Number of People with Limited English Proficiency',font=dict(size=28)),
                  yaxis=dict(title=dict(text='# People',font=dict(size=18)),
                             tickfont=dict(size=14))
                  )
    language_fig.update_xaxes(tickfont=dict(size=14))
    language_fig.update_layout(hovermode='x',showlegend=False)
    
    #B11001 Household type
    housing_url = census_api_url+'?get=group(B11001)'+geography
    housing_data = pd.read_csv(housing_url)
    housing_data = housing_data.drop(columns=housing_data.columns[housing_data.columns.str.contains('A')])
    housing_data = housing_data.drop(columns=['GEO_ID','state','county','county subdivision]','Unnamed: 41'])
    housing_data = housing_data.rename(columns={'[["B11001_001E"':'Total Households',
                                                'B11001_001M':'Total Households Margin of Error',
                                                'B11001_002E':'Family households',
                                                'B11001_002M':'Family households Margin of Error',
                                                'B11001_003E':'Married-couple family',
                                                'B11001_003M':'Married-couple family Margin of Error',
                                                'B11001_004E':'Other family',
                                                'B11001_004M':'Other family Margin of Error',
                                                'B11001_005E':'Male householder, no spouse present',
                                                'B11001_005M':'Male householder, no spouse present Margin of Error',
                                                'B11001_006E':'Female householder, no spouse present',
                                                'B11001_006M':'Female householder, no spouse present Margin of Error',
                                                'B11001_007E':'Nonfamily households',
                                                'B11001_007M':'Nonfamily households Margin of Error',
                                                'B11001_008E':'Householder living alone',
                                                'B11001_008M':'Householder living alone Margin of Error',
                                                'B11001_009E':'Householder not living alone',
                                                'B11001_009M':'Householder not living alone Margin of Error'
                                                })
    housing_data['Total Households'] = housing_data['Total Households'].str[2:-1].astype('int')
    housing_data['Single parent'] = housing_data.loc[0,['Male householder, no spouse present','Female householder, no spouse present']].sum()
    
    housing_cols = ['Married-couple family','Single parent',
                    'Householder living alone','Householder not living alone']
    
    housing_fig = make_subplots(1,2)
    housing_fig.add_trace(go.Bar(x=housing_data[housing_cols].columns,
                            y=housing_data.loc[0,housing_cols],
                            name='Households by Type'
                            ))
    housing_fig.update_layout(title=dict(text='Number of Households by Type',font=dict(size=28)),
                  yaxis=dict(title=dict(text='# Households',font=dict(size=18)),
                             tickfont=dict(size=14))
                  )
    housing_fig.update_xaxes(tickfont=dict(size=14))
    housing_fig.update_layout(hovermode='x',showlegend=False)
    
    #B08301 Means of transportation to work
    #B08303 Travel time to work
    #B08014 Vehicles available
    transportation_url = census_api_url+'?get=group(B08301)'+geography
    transportation_data = pd.read_csv(transportation_url)
    transportation_data = transportation_data.drop(columns=transportation_data.columns[transportation_data.columns.str.contains('A')])
    transportation_data = transportation_data.drop(columns=['GEO_ID','state','county','county subdivision]','Unnamed: 89'])
    transportation_data = transportation_data.rename(columns={'[["B08301_001E"':'Total workers 16 years and over',
                                                              'B08301_001M':'Total workers 16 years and over Margin of Error',
                                                              'B08301_003E':'Drove alone',
                                                              'B08301_003M':'Drove alone Margin of Error',
                                                              'B08301_004E':'Carpooled',
                                                              'B08301_004M':'Carpooled Margin of Error',
                                                              'B08301_010E':'Public transportation',
                                                              'B08301_010M':'Public transportation Margin of Error',
                                                              'B08301_016E':'Taxicab',
                                                              'B08301_016M':'Taxicab Margin of Error',
                                                              'B08301_017E':'Motorcycle',
                                                              'B08301_017M':'Motorcycle Margin of Error',
                                                              'B08301_018E':'Bicycle',
                                                              'B08301_018M':'Bicycle Margin of Error',
                                                              'B08301_019E':'Walked',
                                                              'B08301_019M':'Walked Margin of Error',
                                                              'B08301_020E':'Other means',
                                                              'B08301_020M':'Other means Margin of Error',
                                                              'B08301_021E':'Worked from home',
                                                              'B08301_021M':'Worked from home Margin of Error'})
    transportation_data = transportation_data.drop(columns=transportation_data.columns[transportation_data.columns.str.contains('B08301')])
    transportation_data['Other'] = transportation_data.loc[0,['Taxicab','Motorcycle','Bicycle','Other means']]
    
    trans_means_cols = ['Drove alone','Carpooled','Public transportation','Walked','Other','Worked from home']
    
    transportation2_url = census_api_url+'?get=group(B08303)'+geography
    transportation2_data = pd.read_csv(transportation2_url)
    transportation2_data = transportation2_data.drop(columns=transportation2_data.columns[transportation2_data.columns.str.contains('A')])
    transportation2_data = transportation2_data.drop(columns=['GEO_ID','state','county','county subdivision]','Unnamed: 57'])
    transportation2_data = transportation2_data.rename(columns={'[["B08303_001E"':'Total workers 16 years and over (Time)',
                                                              'B08303_001M':'Total workers 16 years and over (Time) Margin of Error',
                                                              'B08303_002E':'Less than 5 minutes',
                                                              'B08303_002M':'Less than 5 minutes Margin of Error',
                                                              'B08303_003E':'5 to 9 minutes',
                                                              'B08303_003M':'5 to 9 minutes Margin of Error',
                                                              'B08303_004E':'10 to 14 minutes',
                                                              'B08303_004M':'10 to 14 minutes Margin of Error',
                                                              'B08303_005E':'15 to 19 minutes',
                                                              'B08303_005M':'15 to 19 minutes Margin of Error',
                                                              'B08303_006E':'20 to 24 minutes',
                                                              'B08303_006M':'20 to 24 minutes Margin of Error',
                                                              'B08303_007E':'25 to 29 minutes',
                                                              'B08303_007M':'25 to 29 minutes Margin of Error',
                                                              'B08303_008E':'30 to 34 minutes',
                                                              'B08303_008M':'30 to 34 minutes Margin of Error',
                                                              'B08303_009E':'35 to 39 minutes',
                                                              'B08303_009M':'35 to 39 minutes Margin of Error',
                                                              'B08303_010E':'40 to 44 minutes',
                                                              'B08303_010M':'40 to 44 minutes Margin of Error',
                                                              'B08303_011E':'45 to 59 minutes',
                                                              'B08303_011M':'45 to 59 minutes Margin of Error',
                                                              'B08303_012E':'60 to 89 minutes',
                                                              'B08303_012M':'60 to 89 minutes Margin of Error',
                                                              'B08303_013E':'90 or more minutes',
                                                              'B08303_013M':'90 or more minutes Margin of Error'})
    transportation2_data['Less than 15 minutes'] = transportation2_data.loc[0,['Less than 5 minutes','5 to 9 minutes','10 to 14 minutes']].sum()
    transportation2_data['15 to 29 minutes'] = transportation2_data.loc[0,['15 to 19 minutes','20 to 24 minutes','25 to 29 minutes']].sum()
    transportation2_data['30 to 44 minutes'] = transportation2_data.loc[0,['30 to 34 minutes','35 to 39 minutes','40 to 44 minutes']].sum()
    transportation2_data['45 minutes or more'] = transportation2_data.loc[0,['45 to 59 minutes','60 to 89 minutes','90 or more minutes']].sum()
    
    trans_time_cols = ['Less than 15 minutes','15 to 29 minutes','30 to 44 minutes','45 minutes or more']
    
    transportation_fig = make_subplots(1,2)
    transportation_fig.add_trace(go.Bar(x=transportation_data[trans_means_cols].columns,
                            y=transportation_data.loc[0,trans_means_cols],
                            name='Commutes by Type'
                            ),row=1,col=1)
    transportation_fig.add_trace(go.Bar(x=transportation2_data[trans_time_cols].columns,
                            y=transportation2_data.loc[0,trans_time_cols],
                            name='Commutes by Time'
                            ),row=1,col=2)
    transportation_fig.update_layout(title=dict(text='Number of People by Commuting Characteristics',font=dict(size=28)),
                  yaxis=dict(title=dict(text='# People',font=dict(size=18)),
                             tickfont=dict(size=14)),
                  yaxis2=dict(title=dict(text='# People',font=dict(size=18)),
                             tickfont=dict(size=14))
                  )
    transportation_fig.update_xaxes(tickfont=dict(size=14))
    transportation_fig.update_layout(hovermode='x',showlegend=False)
    
    data = pd.concat([income_data,med_inc_data,age_data,education_data,disability_data,language_data,housing_data,transportation_data],axis=1)    
    
    return data, income_fig, age_fig, edu_fig, disability_fig, language_fig, housing_fig, transportation_fig

data, income_fig, age_fig, education_fig, disability_fig, language_fig, housing_fig, transportation_fig = load_data()

with st.expander('Maynard, Environmental Justice and Income'):
    st.write('Map of Maynard, census tracts, EJ info and income data will go here.')
    st.write('Maynard has a population of '+str(data.loc[0,'Total Population'])+' people living in '+str(data.loc[0,'Total Households'])+' households.')
    st.write('Maynard is composed of two census tracts and seven block groups. \
             One block group has been designated by the state as an environmental \
            justice community based on its median household income. Households \
            with lower incomes are more vulnerable to the impacts of climate change.')
    #st.table(income_data[income_cols])
    st.plotly_chart(income_fig)
    st.write('Note: 2022 is the latest year data is available from the U.S. Census Bureau.\
             The U.S. Census Bureau uses two "tracts" and seven "block groups" \
            to represent the Town of Maynard. These are developed to create \
            areas across the country with similar amounts of people for \
            comparison and analysis.')


with st.expander('Race and Ethnicity in Maynard'):
    st.write('Racial and ethnicity data will go here.')


with st.expander('Education in Maynard'):
    st.write('Data on educational attainment, school enrollment, high needs and other stats will go here.')
    st.plotly_chart(education_fig)


with st.expander('Disabilities in Maynard'):
    st.write('Data on disabilities, maybe theres another way to approach this or other data to combine here?')
    st.plotly_chart(disability_fig)


with st.expander('Languages in Maynard'):
    st.write('What languages do we speak in Maynard?')
    st.plotly_chart(language_fig)


with st.expander('Housing in Maynard'):
    st.write('Household types, housing cost and insecurity')
    st.plotly_chart(housing_fig)


with st.expander('Food insecurity in Maynard'):
    st.write('Food insecurity data goes here')


with st.expander('Energy insecurity in Maynard'):
    st.write('Energy consumption and insecurity data will go here')


with st.expander('Transportation in Maynard'):
    st.write('Transporation access, burden, commuting and other data will go here.')
    st.plotly_chart(transportation_fig)

