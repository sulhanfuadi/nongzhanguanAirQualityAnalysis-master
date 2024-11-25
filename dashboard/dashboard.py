# FILE: dashboard.py

# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title and Author Information
st.set_page_config(page_title="Air Quality Analysis at Nongzhanguan Station (2013-2017)")
st.title('Air Quality Analysis at Nongzhanguan Station (2013-2017)')
st.write("""
**Author**: [Sulhan Fuadi](https://www.linkedin.com/in/sulhanfuadi/) \n
**GitHub**: [Sulhan Fuadi](https://github.com/sulhanfuadi)
""")

# Project Overview
# Project Overview
st.header('Project Overview')

st.write("""
This project analyzes air quality at Nongzhanguan Station from 2013 to 2017, focusing on pollutants like PM2.5, PM10, SO2, NO2, CO, O3, and environmental factors such as temperature, air pressure, wind speed, and precipitation. The analysis includes data loading, cleaning, exploratory data analysis, binning, and drawing conclusions.
""")

# Load the dataset
data_url = './data/PRSA_Data_Nongzhanguan_20130301-20170228.csv'
data = pd.read_csv(data_url)
st.subheader('Data Overview')
st.write(data.head())

# Cleaning the data by handling missing values
# Missing values will be handled using forward fill, and a datetime index will be created.
data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])
data.set_index('datetime', inplace=True)
data_cleaned = data.fillna(method='ffill')

# Exploratory Data Analysis (EDA)
st.header('Exploratory Data Analysis (EDA)')

# Summary Statistics
st.subheader('Summary Statistics')
st.write("Below are the summary statistics for the numerical variables in the dataset:")
st.write(data_cleaned.describe())

# Distribution of Air Quality Variables
st.subheader('Distribution of Air Quality Variables')
fig, axes = plt.subplots(3, 2, figsize=(14, 12))
sns.histplot(data_cleaned['PM2.5'].dropna(), bins=50, kde=True, ax=axes[0, 0])
axes[0, 0].set_title('PM2.5 Distribution')
sns.histplot(data_cleaned['PM10'].dropna(), bins=50, kde=True, ax=axes[0, 1])
axes[0, 1].set_title('PM10 Distribution')
sns.histplot(data_cleaned['NO2'].dropna(), bins=50, kde=True, ax=axes[1, 0])
axes[1, 0].set_title('NO2 Distribution')
sns.histplot(data_cleaned['CO'].dropna(), bins=50, kde=True, ax=axes[1, 1])
axes[1, 1].set_title('CO Distribution')
sns.histplot(data_cleaned['TEMP'].dropna(), bins=50, kde=True, ax=axes[2, 0])
axes[2, 0].set_title('Temperature Distribution')
sns.histplot(data_cleaned['WSPM'].dropna(), bins=50, kde=True, ax=axes[2, 1])
axes[2, 1].set_title('Wind Speed Distribution')
plt.tight_layout()
st.pyplot(fig)

# PM2.5 trends over time
st.subheader('Explore PM2.5 Trends Over Time')
monthly_pm25 = data_cleaned['PM2.5'].resample('M').mean()
plt.figure(figsize=(10, 6))
plt.plot(monthly_pm25.index, monthly_pm25, label='PM2.5 (Monthly Avg)', color='royalblue', linewidth=2, marker='o')
plt.title('Monthly Average PM2.5 Levels (2013-2017)', fontsize=14)
plt.xlabel('Date (Month-Year)', fontsize=12)
plt.ylabel('PM2.5 Concentration (µg/m³)', fontsize=12)
plt.grid(True)
plt.legend(loc='upper right')
st.pyplot(plt)

# Correlation Matrix
st.subheader('Correlation Matrix of Air Quality and Meteorological Variables')
corr_matrix = data_cleaned[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'WSPM']].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
ax.set_title('Correlation Matrix of Air Quality and Meteorological Variables')
st.pyplot(fig)

# Time Series Analysis
st.subheader('Time Series Analysis of PM2.5, PM10, and NO2')
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(data_cleaned.index, data_cleaned['PM2.5'], label='PM2.5', alpha=0.6)
ax.plot(data_cleaned.index, data_cleaned['PM10'], label='PM10', alpha=0.6)
ax.plot(data_cleaned.index, data_cleaned['NO2'], label='NO2', alpha=0.6)
ax.set_title('Time Series of PM2.5, PM10, and NO2')
ax.set_xlabel('Time')
ax.set_ylabel('Concentration')
ax.legend()
plt.tight_layout()
st.pyplot(fig)

# Monthly Average PM2.5 Levels
st.subheader('Monthly Average PM2.5 Levels')
monthly_pm25 = data_cleaned['PM2.5'].resample('M').mean()
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_pm25.index, monthly_pm25, label='PM2.5 (Monthly Avg)', color='royalblue', linewidth=1.5, marker='o', markersize=6, markerfacecolor='white', markeredgewidth=1.5, markeredgecolor='royalblue')
ax.set_title('Monthly Average PM2.5 Levels at Nongzhanguan Station')
ax.set_xlabel('Date (Month-Year)')
ax.set_ylabel('PM2.5 Concentration (µg/m³)')
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.legend(loc='upper right')
plt.tight_layout()
st.pyplot(fig)

# Annual Trends of PM2.5 and Temperature
st.subheader('Annual Trends of PM2.5 and Temperature')
annual_pm25 = data_cleaned['PM2.5'].resample('Y').mean()
annual_temp = data_cleaned['TEMP'].resample('Y').mean()
fig, ax1 = plt.subplots(figsize=(10, 6))
line1 = ax1.plot(annual_pm25.index, annual_pm25, color='blue', marker='o', linewidth=2, label='PM2.5 (Annual Avg)')
ax1.set_xlabel('Year')
ax1.set_ylabel('PM2.5 Concentration (µg/m³)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax2 = ax1.twinx()
line2 = ax2.plot(annual_temp.index, annual_temp, color='red', marker='o', linewidth=2, label='Temperature (Annual Avg)')
ax2.set_ylabel('Temperature (°C)', color='red')
ax2.tick_params(axis='y', labelcolor='red')
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
plt.title('Annual Trends of PM2.5 and Temperature (2013-2017)')
plt.tight_layout()
st.pyplot(fig)

# Correlation Matrix for PM2.5 and Temperature
st.subheader('Correlation Matrix for PM2.5 and Temperature')
correlation_columns = ['PM2.5', 'TEMP']
correlation_matrix = data_cleaned[correlation_columns].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, vmin=-1, vmax=1, square=True, ax=ax)
ax.set_title('Correlation Matrix for PM2.5 and Temperature')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
st.pyplot(fig)

# Conclusion
st.header('Conclusion')
st.write("""
The analysis of PM2.5 and temperature trends at Nongzhanguan Station (2013-2017) reveals significant seasonal peaks in PM2.5 levels, particularly during winter due to increased coal combustion, with no long-term downward trend despite some short-term improvements. Temperature trends were stable, with a notable anomaly in 2017, but showed a weak correlation with PM2.5 levels, emphasizing the dominant role of human activities such as industrial emissions and traffic pollution. The findings highlight the need for consistent, year-round pollution control measures, clean energy transitions, advanced monitoring, and public engagement to achieve sustainable air quality improvements.
""")

st.write("Thank you for exploring the air quality analysis at Nongzhanguan Station!")
