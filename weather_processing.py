"""
Created on Mon Feb  7 14:10:42 2022

@author: Okhrimchuk Roman
for Sierentz Global Merchants

Test task
"""

# TODO Import the necessary libraries

import pandas as pd
import numpy as np
import pathlib
from datetime import date
import warnings
import seaborn as sns
warnings.filterwarnings('ignore')

# TODO Import the dataset 

path = r'./data/weather_dataset.data'
data=pd.read_csv(path, on_bad_lines='skip', header=0, sep='\s+')
pd.options.display.float_format = "{:,.2f}".format

# check information about type of data and non-null values
data.info() 

# TODO  Assign it to a variable called data and replace the first 3 columns by a proper datetime index

data[['Yr', 'Mo', 'Dy']]=data[['Yr', 'Mo', 'Dy']].astype(str)
data['date']=data[['Yr', 'Mo', 'Dy']].agg('-'.join, axis=1)
data.date=pd.to_datetime(data.date)
data.drop(['Yr', 'Mo', 'Dy'], axis=1, inplace=True)

# TODO Set the right dates as the index. Pay attention at the data type, it should be datetime64[ns]

data.set_index('date', inplace=True)

# TODO Check if everything is okay with the data. Create functions to delete/fix rows with strange cases and apply them

# changing types of data to float
for column in data.columns:
    data[column]=pd.to_numeric(data[column].str.replace(',', '.'), errors='coerce', downcast='float')
    
# searching for strange data using boxplot

data_stack=pd.DataFrame(data.stack().reset_index()).rename(columns={'level_1':'location', 0:'windspeed'})
g = sns.FacetGrid(data=data_stack, col='location', col_wrap=4, sharex=False)
g.map(sns.boxplot, 'windspeed')

# As can be seen from graphs there are two types of strange data: negative value in 'loc11' column and enormous value in 'loc9' column

# Function for fixing strange cases

def data_check(data):
    for column in data.columns:
        data[column].mask((data[column]<0) | (data[column]>100), np.nan, inplace=True)
    return data
  
data_check(data)
    
# TODO Write a function in order to fix date (this relate only to the year info) and apply it

now=date.today().year
def fixing_dates(data):
    fix_date=pd.Series([])
    for i in pd.DatetimeIndex(data.index):
        if i.year>now:
            year=i.year-100
            dat=pd.Series([i.replace(year=year)])
            fix_date=pd.concat([fix_date, dat], axis=0)
        else:
            dat=pd.Series(i)
            fix_date=pd.concat([fix_date, dat], axis=0)
    data.index=fix_date
    return data

fixing_dates(data)

# TODO Compute how many values are missing for each location over the entire record

for column in data.columns:
    try:
        null_values=(data[column].isna()==True).value_counts()[1]
        print (f'{column} : null values - {null_values}')
    except KeyError:
        print (f'{column} : null values - 0')

# TODO Compute how many non-missing values there are in total

data.info()

# Filling missing values

data.fillna(method='ffill', inplace=True)  # filling missing values with values from previous date
data.fillna(method='bfill', inplace=True)  # filling missing values from first date in data set with values from next date

# TODO Calculate the mean windspeeds of the windspeeds over all the locations and all the times

mean_windspeed=np.round(sum(data.mean())/len(data.columns), decimals=2)

# TODO Create a DataFrame called loc_stats and calculate the min, max and mean windspeeds and standard deviations of the windspeeds at each location over all the days

loc_stats=data.describe().loc[['min','max', 'min', 'std']]

# TODO Find the average windspeed in January for each location

january_mean=pd.DataFrame(data[pd.DatetimeIndex(data.index).month==1].reset_index(drop=True).mean(),
                          index=data.columns, columns=['mean'])

# TODO Downsample the record to a yearly frequency for each location

annual_stat=data.resample('A').mean()

# TODO Downsample the record to a monthly frequency for each location

month_stat=data.resample('M').mean()

# TODO Downsample the record to a weekly frequency for each location

week_stat=data.resample('W').mean()

# TODO Calculate the min, max and mean windspeeds and standard deviations of the windspeeds across all locations for each week (assume that the first week starts on January 2 1961) for the first 21 weeks

stat_21weeks=data.loc['1961-01-02':, :].resample('W').agg(['min','mean', 'max', 'std'])[:21].stack(level=-1)
