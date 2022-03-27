# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 09:33:51 2022

@author: gixi_
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(layout="wide")


st.write("Welcome to our Dashboard - Patients Survivals Dataset")

patients = pd.read_csv(r'C:\Users\gixi_\Downloads\ironhack data export/patients.csv')


st.write(patients)


#Gender and Age Distribution by Box Plot
fig5 = plt.figure(figsize=(12,6))
sns.boxplot(x='age',y='gender',data=patients).set(title ="Gender and Age Distribution")
st.pyplot(fig5)

   
        
#The total of hospital per apache_3j_bodysystem

apache3_hospital=patients[['apache_3j_bodysystem','hospital_id']].groupby('apache_3j_bodysystem').agg({'hospital_id':'count'})
apache3_hospital.rename({'hospital_id': 'number of hospitals'}, axis=1, inplace=True)
apache3_hospital.sort_values(by="number of hospitals",inplace=True) 

st.header("The total of hospital per apache_3j_bodysystem")
plt.figure(figsize=(20,10))   
st.bar_chart(apache3_hospital)



#Age histogram

hist_age = sns.displot(patients['age']).set(title ="Distribution of patients'ages")
plt.figure(figsize=(8,6))
hist_age.set( xlabel = "Age", ylabel = "Frequencies")
st.pyplot(hist_age)



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
b1

labels = b1['icu_admit_source']
sizes =b1['quantities']
explode = (0, 0.1, 0, 0, 0)
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=40)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1,height=300)


#gender per disease

diseases = patients[['gender','aids','cirrhosis','diabetes_mellitus','hepatic_failure','immunosuppression','leukemia','lymphoma','solid_tumor_with_metastasis']]
diseases = diseases.groupby('gender').sum().transpose()

fig = px.bar(diseases, x=diseases.index, y=['F', 'M'], barmode='group', title ="Number of patient per disease per gender")
fig.update_yaxes(title_text='Number of patient')
fig.update_xaxes(title_text="Diseases")
st.plotly_chart(fig)

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
fig2, ax2 = plt.subplots()
ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=40)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig2,height=300)



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
b5

labels = b5['bmi_classification']
sizes = b5[bar_axis2]
explode = (0, 0.1, 0, 0)
fig3, ax3 = plt.subplots()
ax3.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=40)
ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig3,height=200)


#BMI Distribution per gender

fig4, ax4 = plt.subplots()
sns.distplot(patients[(patients['gender']=='F')&(patients['diabetes_mellitus']==1)]['bmi'],  kde=False, label='Female BMI')
sns.distplot(patients[(patients['gender']=='M')&(patients['diabetes_mellitus']==1)]['bmi'],  kde=False, label='Male BMI')

plt.title('Comparing the bmi distribution between the males and gemales')
plt.xlabel('BMI')
plt.ylabel('Density')
plt.legend()
st.pyplot(fig4)

#Correlation

heatmap_fig = plt.figure(figsize=(12,6))
fig = sns.heatmap(patients[['age',
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
st.pyplot(heatmap_fig)

heatmap_fig1 = plt.figure(figsize=(20,10))
sns.heatmap(patients[['apache_post_operative',
       'arf_apache', 'gcs_eyes_apache', 'gcs_motor_apache',
       'gcs_unable_apache', 'gcs_verbal_apache', 'heart_rate_apache',
       'intubated_apache', 'map_apache', 'resprate_apache', 'temp_apache',
       'ventilated_apache']].corr(),annot=True,cmap="viridis")

st.pyplot(heatmap_fig1)


