# FILE: dashboard.py

# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title and Author Information
st.title('Air Quality Analysis at Nongzhanguan Station (2013-2017)')
st.write("""
**Author**: Sulhan Fuadi \n
**GitHub**: [Sulhan Fuadi](https://github.com/sulhanfuadi)
""")

# Project Overview
st.header('Project Overview')

st.write("""
The aim of this project is to perform a thorough analysis of air quality at Nongzhanguan Station, concentrating on various pollutants and environmental factors. The pollutants of interest include:

- **PM2.5** - Fine particulate matter with a diameter less than 2.5 micrometers.
- **PM10** - Coarse particulate matter with a diameter less than 10 micrometers.
- **SO2** - Sulfur dioxide.
- **NO2** - Nitrogen dioxide.
- **CO** - Carbon monoxide.
- **O3** - Ozone.
- **Environmental factors** - Temperature, air pressure, wind speed, and precipitation.

This notebook provides a comprehensive analysis of air quality data from Nongzhanguan Station for the period from 2013 to 2017.

We will follow these steps to conduct the analysis:
- Data Loading: Importing the dataset and preparing it for analysis.
- Data Cleaning and Wrangling: Handling missing values and transforming the data as needed.
- Exploratory Data Analysis (EDA): Visualizing and summarizing the data to uncover patterns and insights.
- Binning Analysis: Categorizing data into bins to facilitate further analysis.
- Conclusion: Summarizing the findings and drawing conclusions based on the analysis.
""")

st.subheader('Business Questions')
st.write("""
1. What are the trends in PM2.5 levels at Nongzhanguan Station from 2013 to 2017?  
2. How do temperature variations correlate with PM2.5 levels?
""")

# Load the dataset
st.subheader('Load the Air Quality Dataset')
data_url = './PRSA_Data_Nongzhanguan_20130301-20170228.csv'
data = pd.read_csv(data_url)
st.write('Preview of the dataset:')
st.write(data.head())

# Data Wrangling Section
st.header('Data Wrangling')

# Gathering Data
st.subheader('Gathering Data')
st.write("We will gather the dataset, which includes air quality measurements for pollutants and environmental factors.")

# Missing Data Analysis
st.subheader('Assessing Data')
st.write("Checking for missing values and ensuring data quality.")
missing_values = data.isnull().sum()
st.write('Missing values in the dataset:')
st.write(missing_values)

# Cleaning the data by handling missing values
st.subheader('Cleaning Data')
st.write("""
Missing values will be handled using forward fill, and a datetime index will be created.
""")
data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])
data.set_index('datetime', inplace=True)
data_cleaned = data.fillna(method='ffill')
st.write('Preview of cleaned data:')
st.write(data_cleaned.head())

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
# st.subheader('Monthly Average PM2.5 Levels')
# monthly_pm25 = data_cleaned['PM2.5'].resample('M').mean()
# fig, ax = plt.subplots(figsize=(10, 6))
# ax.plot(monthly_pm25.index, monthly_pm25, label='PM2.5 (Monthly Avg)', color='royalblue', linewidth=1.5, marker='o', markersize=6, markerfacecolor='white', markeredgewidth=1.5, markeredgecolor='royalblue')
# ax.set_title('Monthly Average PM2.5 Levels at Nongzhanguan Station')
# ax.set_xlabel('Date (Month-Year)')
# ax.set_ylabel('PM2.5 Concentration (µg/m³)')
# ax.grid(True, which='both', linestyle='--', linewidth=0.5)
# ax.legend(loc='upper right')
# plt.tight_layout()
# st.pyplot(fig)

# Annual Trends of PM2.5 and Temperature
# st.subheader('Annual Trends of PM2.5 and Temperature')
# annual_pm25 = data_cleaned['PM2.5'].resample('Y').mean()
# annual_temp = data_cleaned['TEMP'].resample('Y').mean()
# fig, ax1 = plt.subplots(figsize=(10, 6))
# line1 = ax1.plot(annual_pm25.index, annual_pm25, color='blue', marker='o', linewidth=2, label='PM2.5 (Annual Avg)')
# ax1.set_xlabel('Year')
# ax1.set_ylabel('PM2.5 Concentration (µg/m³)', color='blue')
# ax1.tick_params(axis='y', labelcolor='blue')
# ax2 = ax1.twinx()
# line2 = ax2.plot(annual_temp.index, annual_temp, color='red', marker='o', linewidth=2, label='Temperature (Annual Avg)')
# ax2.set_ylabel('Temperature (°C)', color='red')
# ax2.tick_params(axis='y', labelcolor='red')
# lines = line1 + line2
# labels = [l.get_label() for l in lines]
# ax1.legend(lines, labels, loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
# plt.title('Annual Trends of PM2.5 and Temperature (2013-2017)')
# plt.tight_layout()
# st.pyplot(fig)

# Correlation Matrix for PM2.5 and Temperature
# st.subheader('Correlation Matrix for PM2.5 and Temperature')
# correlation_columns = ['PM2.5', 'TEMP']
# correlation_matrix = data_cleaned[correlation_columns].corr()
# fig, ax = plt.subplots(figsize=(8, 6))
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, vmin=-1, vmax=1, square=True, ax=ax)
# ax.set_title('Correlation Matrix for PM2.5 and Temperature')
# plt.xticks(rotation=45, ha='right')
# plt.yticks(rotation=0)
# plt.tight_layout()
# st.pyplot(fig)

# Visualization & Explanatory Analysis
st.header('Visualization & Explanatory Analysis')

st.subheader('Question 1: What are the trends in PM2.5 levels at Nongzhanguan Station from 2013 to 2017?')

st.subheader('PM2.5 Levels at Nongzhanguan Station (2013-2017)')
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

st.write("""
The analysis of PM2.5 levels at Nongzhanguan Station from 2013 to 2017 reveals several key trends:

- **Fluctuating Patterns**: PM2.5 levels exhibit significant fluctuations over the years, with notable peaks and troughs.
- **Early 2014**: There is a significant spike in PM2.5 levels, reaching over 150 µg/m³.
- **Mid-2014**: PM2.5 levels drop significantly, stabilizing around 60-80 µg/m³.
- **Late 2015 to Early 2016**: Another sharp increase in PM2.5 levels is observed, peaking above 160 µg/m³.
- **Mid-2016**: PM2.5 levels decrease again to around 60 µg/m³.
- **Overall Trend**: Despite the fluctuations, there is no clear long-term downward trend in PM2.5 levels, indicating that high levels of pollution persisted throughout the period.

These observations highlight the variability in PM2.5 concentrations over the years, with periods of both high and low pollution. The lack of a clear downward trend suggests that persistent pollution issues remain, necessitating ongoing efforts to address and mitigate PM2.5 pollution at Nongzhanguan Station.
        """)

# Correlation Heatmap
st.subheader('Question 2: How do temperature variations correlate with PM2.5 levels?')

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

st.subheader('Correlation Matrix for PM2.5 and Temperature')
correlation_matrix_temp = data_cleaned[['PM2.5', 'TEMP']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix_temp, annot=True, cmap='coolwarm', linewidths=0.5, vmin=-1, vmax=1, square=True)
plt.title('Correlation Between PM2.5 and Temperature', fontsize=14, pad=12)
st.pyplot(plt)

st.write("""
The analysis reveals a weak correlation between temperature and PM2.5 levels, as indicated by a low correlation coefficient (close to 0). This suggests that changes in temperature do not have a strong direct impact on PM2.5 concentrations. 

To further explore this relationship, we utilized scatter plots and a correlation matrix:

- **Scatter Plot**: The scatter plot of temperature versus PM2.5 levels shows a dispersed pattern with no clear trend, reinforcing the weak correlation.
- **Correlation Matrix**: The correlation matrix quantifies the relationship, confirming that the correlation coefficient between temperature and PM2.5 is low.

These findings imply that while temperature is an important meteorological factor, it does not significantly influence PM2.5 levels. Instead, other factors such as industrial emissions, vehicular traffic, and seasonal activities (e.g., heating during winter) may have a more substantial impact on PM2.5 concentrations.

Understanding this weak correlation helps us focus on identifying and mitigating the primary sources of PM2.5 pollution. It suggests that efforts to improve air quality should prioritize controlling emissions from key sources rather than relying solely on temperature-related interventions.
        """)

# Conclusion
st.header('Conclusion')
st.write("""
Comprehensive Conclusion of PM2.5 and Temperature Analysis (2013-2017)

1. **Key Findings on PM2.5 Trends**  
The analysis of PM2.5 concentrations at Nongzhanguan Station between 2013 and 2017 provides crucial insights into the patterns and challenges of air pollution:  

- **Fluctuations and Seasonal Peaks**  
  PM2.5 levels showed notable variability, with significant peaks in early 2014 and from late 2015 to early 2016. These peaks were likely driven by seasonal heating activities and possibly emission-intensive events. Winter months consistently recorded the highest pollution levels due to increased coal combustion and atmospheric conditions that trap pollutants.  

- **Persistent Pollution Levels**  
  Despite some improvements in mid-2014 and mid-2015, there was no long-term downward trend in PM2.5 concentrations. This suggests that existing pollution control efforts were either insufficient or inconsistently applied over time.  

- **Short-Term Improvements and Sustainability Challenges**  
  The temporary reductions in pollution highlight the potential effectiveness of targeted interventions. However, the recurring peaks underscore the need for more sustained and comprehensive measures to achieve meaningful air quality improvements.  

2. **Temperature Trends and Their Implications**  
- **Stable Climatic Conditions**  
  Temperature trends during the period were relatively stable, with only minor year-to-year variations. This consistency provides a reliable baseline for analyzing the impact of temperature on PM2.5 levels.  

- **2017 Temperature Anomaly**  
  A sharp temperature increase in 2017 deviated from earlier patterns. Despite this anomaly, no significant relationship was observed between the temperature rise and PM2.5 levels, indicating that other factors primarily drive pollution dynamics.  

3. **Weak Correlation Between PM2.5 and Temperature**  
- **Minimal Direct Influence**  
  Statistical analysis revealed a weak correlation between temperature and PM2.5 concentrations. While temperature might affect the dispersion of pollutants, it is not a primary driver of PM2.5 levels.  

- **Dominant Role of Human Activities**  
  The findings emphasize the significant impact of industrial emissions, traffic pollution, and seasonal heating activities. These factors far outweigh the influence of temperature variations on PM2.5 levels.  

4. **Broader Implications for Pollution Control and Policy Development**  
- **Complexity of Air Pollution Dynamics**  
  The absence of a clear downward trend in PM2.5 concentrations highlights the intricate nature of urban air pollution, where multiple factors interact in dynamic ways.  

- **Policy and Enforcement Gaps**  
  Temporary improvements in PM2.5 levels during certain periods demonstrate that targeted interventions can work. However, the recurrence of pollution peaks points to gaps in the consistency, enforcement, and scope of pollution control policies.  

Final Thought: A Path Towards Sustainable Air Quality Management  

The analysis underscores that improving air quality requires a multi-dimensional strategy addressing both human-induced and natural factors. While temperature trends during 2013–2017 had limited impact on PM2.5 levels, the dominant influence of anthropogenic activities highlights the urgency of sustained interventions. Key recommendations include:  

- **Year-Round Pollution Control**  
  Implement consistent measures to reduce emissions throughout the year, with a focus on winter months when pollution is most severe.  

- **Clean Energy Transition and Traffic Management**  
  Promote cleaner energy sources for heating and industrial processes while incentivizing the use of electric vehicles and public transportation to reduce vehicular emissions.  

- **Advanced Monitoring and Policy Enforcement**  
  Strengthen air quality monitoring systems to identify pollution sources in real-time and enable more effective policy implementation.  

- **Public Engagement and Awareness**  
  Conduct educational campaigns to increase public understanding of air pollution's health risks and encourage sustainable behaviors.  

Achieving sustainable air quality improvement demands collaborative efforts from policymakers, industries, and the public. By addressing pollution sources holistically and persistently, we can reduce PM2.5 levels, protect public health, and foster a cleaner, more sustainable environment for the future.  
""")

st.write("Thank you for exploring the air quality analysis at Nongzhanguan Station!")