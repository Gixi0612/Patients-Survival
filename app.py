# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 15:51:03 2022

@author: gixi_
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(layout="wide")


st.write("Patients Survival Dashboard")

uploaded_file= st.file_uploader("Choose a file")
if uploaded_file is None:
  st.write("Please upload the file")
  
else:
  patients = pd.read_csv(uploaded_file)
  patients.drop(['Unnamed: 0'], axis = 1, inplace = True)
  st.write(patients)
  #Gender and Age Distribution by Box Plot
  fig1 = plt.figure(figsize=(12,6))
  sns.boxplot(x='age',y='gender',data = patients).set(title ="Gender and Age Distribution")
        
        
           
                
    #The total of hospital per apache_3j_bodysystem
        
  apache3_hospital=patients[['apache_3j_bodysystem','hospital_id']].groupby('apache_3j_bodysystem').agg({'hospital_id':'count'})
  apache3_hospital.rename({'hospital_id': 'number of hospitals'}, axis=1, inplace=True)
  apache3_hospital.sort_values(by="number of hospitals",inplace=True) 
    
  st.header("The total of hospital per apache_3j_bodysystem")
  fig2 = plt.figure(figsize=(12,15))   
  st.bar_chart(apache3_hospital)
    
    
    
    #Age histogram
    
  fig3 = sns.displot(patients['age']).set(title ="Distribution of patients'ages")
  plt.figure(figsize=(8,6))
  fig3.set( xlabel = "Age", ylabel = "Frequencies")
  st.pyplot(fig3)
    
    
    #Survival rate by age group for each gender
  tumor=patients.loc[patients.solid_tumor_with_metastasis==1]
  tumor.sort_values(by="age",inplace=True)
  tumor_age=tumor[["group_age","patient_id","gender","survival"]].groupby(["group_age","gender"]).agg({'patient_id':'count','survival':'sum'})
  tumor_age.reset_index(inplace=True)
  tumor_age["survival_rate"]=tumor_age["survival"]/tumor_age["patient_id"]
  gender_select = st.sidebar.selectbox(label="Please select your gender",options=['M','F'])
  fig12=plt.figure(figsize=(8,6))
  plt.plot(tumor_age.loc[tumor_age.gender==gender_select]['survival_rate'])
  plt.title("Tumor survival rate - Selected Gender is {}".format(gender_select))
  plt.xticks(np.arange(0,15,2),['10-20','20-30','30-40','40-50','50-60','60-70','70-80','80-90'])
  plt.xlabel("group_age")
  plt.ylabel("survival_rate")
  st.pyplot(fig12)

    
    #Pie Chart per hospital 
    
  st.sidebar.markdown("### Charts: Different ICU Admit Sources Per Hospital_ID : ")
  pie_chart1 = pd.crosstab(patients.hospital_id, patients.icu_admit_source, margins=True, margins_name="Total")
  hospital_id_options = patients['hospital_id'].unique().tolist()
  bar_axis = st.sidebar.selectbox(label="Please choose the hospital_id",
                                      options=hospital_id_options)
    
    
    
            
  b = pie_chart1.loc[pie_chart1.index==bar_axis]
  b1 = b[['Accident & Emergency','Floor','Operating Room / Recovery','Other Hospital','Other ICU']]
  b1 = b1.reset_index()[['Accident & Emergency','Floor','Operating Room / Recovery','Other Hospital','Other ICU']].transpose()
  b1.rename({0: 'quantities'}, axis=1, inplace=True)
  b1.reset_index(inplace = True)
    
    
  labels = b1['icu_admit_source']
  sizes =b1['quantities']
  explode = (0, 0.1, 0, 0, 0)
  fig4, ax4 = plt.subplots()
  ax4.title.set_text('Different ICU Admit Sources Per Hospital_ID  {}'.format(bar_axis))
  ax4.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=40)
  ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    
    
    #gender per disease
    
  diseases = patients[['gender','aids','cirrhosis','diabetes_mellitus','hepatic_failure','immunosuppression','leukemia','lymphoma','solid_tumor_with_metastasis']]
  diseases = diseases.groupby('gender').sum().transpose()
    
  fig5 = px.bar(diseases, x=diseases.index, y=['F', 'M'], barmode='group', title ="Number of patients per disease per gender")
  fig5.update_yaxes(title_text='Number of patient')
  fig5.update_xaxes(title_text="Diseases")
    
    
    
    #Diabetes_mellitus by gender
  diabetics=patients[['gender','diabetes_mellitus']].groupby('gender').agg({'diabetes_mellitus':'count'})
    
  st.header("Diabetics by gender")
  plt.figure(figsize=(20,10))   
    
    
    
    #disease per ethicinity
  st.sidebar.markdown("### Charts: Different Diseases per Ethnictity : ")
    
  ethnicity_id_options = patients['ethnicity'].unique().tolist()
  bar_axis1 = st.sidebar.selectbox(label="Please choose the Ethnictity",
                                      options=ethnicity_id_options)
    
    
  disease_ethnicity = patients[['ethnicity','aids', 'cirrhosis', 'diabetes_mellitus',
           'hepatic_failure', 'immunosuppression', 'leukemia', 'lymphoma',
           'solid_tumor_with_metastasis']]
    
  pie_chart2 = disease_ethnicity.groupby('ethnicity').sum()
    
    
  b2 = pie_chart2.loc[pie_chart2.index==bar_axis1]
  b3 = b2[['aids', 'cirrhosis', 'diabetes_mellitus',
           'hepatic_failure', 'immunosuppression', 'leukemia', 'lymphoma',
           'solid_tumor_with_metastasis']]
  b3 = b3.reset_index()[['aids', 'cirrhosis', 'diabetes_mellitus',
           'hepatic_failure', 'immunosuppression', 'leukemia', 'lymphoma',
           'solid_tumor_with_metastasis']].transpose()
  b3.rename({0: bar_axis1}, axis=1, inplace=True)
  b3.reset_index(inplace = True)
    
    
  labels = b3['index']
  sizes = b3[bar_axis1]
  explode = (0, 0.1, 0, 0, 0,0,0,0)
  fig6, ax6 = plt.subplots()
  ax6.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=40)
  ax6.title.set_text('Different Diseases per Ethnictity {}'.format(bar_axis1.capitalize()))
  ax6.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    
    
    
    #BMI_classification per disease
    
  st.sidebar.markdown("### Charts: DifferentB BMI Classifications of patients per Diseases : ")
    
  diseases_id_options = ['aids', 'cirrhosis', 'diabetes_mellitus',
           'hepatic_failure', 'immunosuppression', 'leukemia', 'lymphoma',
           'solid_tumor_with_metastasis']
  bar_axis2 = st.sidebar.selectbox(label="Please choose the disease",
                                      options=diseases_id_options)
    
    
  diseases_bmi = patients[['bmi_classification','aids','cirrhosis','diabetes_mellitus','hepatic_failure','immunosuppression','leukemia','lymphoma','solid_tumor_with_metastasis']]
  pie_chart3 = diseases_bmi.groupby('bmi_classification').sum().transpose()
    
  b4 = pie_chart3.loc[pie_chart3.index==bar_axis2]
  b5 = b4[['Healthy Weight','Obesity','Overweight','Underweight']]
  b5 = b5.reset_index()[['Healthy Weight','Obesity','Overweight','Underweight']].transpose()
  b5.rename({0: bar_axis2}, axis=1, inplace=True)
  b5.reset_index(inplace = True)
    
  labels = b5['bmi_classification']
  sizes = b5[bar_axis2]
  explode = (0, 0.1, 0, 0)
  fig7, ax7 = plt.subplots()
  ax7.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=40)
  ax7.title.set_text('DifferentB BMI Classifications of patients per Diseases')
  ax7.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    
    
    #BMI Distribution per gender
    
  fig8, ax8 = plt.subplots()
  sns.distplot(patients[(patients['gender']=='F')&(patients['diabetes_mellitus']==1)]['bmi'],  kde=False, label='Female BMI')
  sns.distplot(patients[(patients['gender']=='M')&(patients['diabetes_mellitus']==1)]['bmi'],  kde=False, label='Male BMI')
    
  plt.title('Comparing the bmi distribution between the males and gemales')
  plt.xlabel('BMI')
  plt.ylabel('Density')
  plt.legend()
    
    
    #Correlation
    
  fig9 = plt.figure(figsize=(12,6))
  sns.heatmap(patients[['age',
     'bmi',
     'elective_surgery',
     'ethnicity',
     'gender',
     'height',
     'icu_admit_source',
     'icu_stay_type',
     'icu_type',
     'pre_icu_los_days',
     'weight','diabetes_mellitus']].corr(),annot=True,cmap="viridis")
    
    
  fig10 = plt.figure(figsize=(20,10))
  sns.heatmap(patients[['apache_post_operative',
           'arf_apache', 'gcs_eyes_apache', 'gcs_motor_apache',
           'gcs_unable_apache', 'gcs_verbal_apache', 'heart_rate_apache',
           'intubated_apache', 'map_apache', 'resprate_apache', 'temp_apache',
           'ventilated_apache']].corr(),annot=True,cmap="viridis")
    
    
  container1 = st.container()
  col1, col2 = st.columns(2)
    
  with container1:
        with col1:
            fig1
        with col2:
            fig4
    
  st.plotly_chart(fig5)
    
  container2 = st.container()
  col3, col4 = st.columns(2)
    
  with container2:
        with col3:
            st.bar_chart(diabetics)
        with col4:
            fig6
    
    
    
  container3 = st.container()
  col5, col6 = st.columns(2)
    
  with container2:
        with col3:
            fig7
        with col4:
            fig8
    
  container4 = st.container()
  col7, col8 = st.columns(2)
    
  with container2:
        with col3:
            fig9
        with col4:
            fig10
    
    
    
    
    
       