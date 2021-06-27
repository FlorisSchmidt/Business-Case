#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import historic
from pathlib import Path
import cityRemap
from sklearn.utils import resample
import numpy as np
import scipy
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys
# In[2]:
os.environ['TMPDIR']

cities = ['AMS','BRU','BSL','DXB','FRA','HKG','HYD','JNB','LIM','NRT','ORD','PVG','SCL','SFO','SIN','SYD','ZRH']
city = sys.argv[1]
# In[3]:



data = pd.read_csv(Path('extracted/high/AMS.csv'))[['dt','Temperature']]
temp = data
temp.dt = pd.DatetimeIndex(temp.dt)
temp = temp.set_index('dt')


# In[4]:


testset = temp[temp.index.year==2020]



# In[5]:


df = pd.DataFrame(
        {'dt': pd.date_range('2021-01-01', '2022-01-01', freq='1H', closed='left')})


# In[6]:


date = pd.DataFrame()
for month in range(1,13):
    month_data = df[df.dt.dt.month==month]
    date = date.append(month_data.iloc[0:24],ignore_index=True)
date = pd.DatetimeIndex(date.dt)


# In[7]:


def get_historical(conf,year):    
    historic_interval = pd.DataFrame()
    historic_data = temp[(temp.index.year>2019-year) & (temp.index.year<2020)]
    #historic_data.index = pd.DatetimeIndex(data.dt)
    for month in range(1,13):
        for hour in range(24):  
                points = historic_data.loc[(historic_data.index.hour==hour) & (historic_data.index.month==month)]
                lower = points['Temperature'].quantile((1-conf)/2)
                higher = points['Temperature'].quantile(1-((1-conf)/2))
                historic_interval = historic_interval.append({'Lower':lower,'Higher':higher}, ignore_index=True)
    historic_interval = historic_interval.set_index(date)
    return historic_interval


# In[8]:


def result(interval_set):
    correct = 0
    total = 0
    for hour in range(24):
        for month in range(1,13):
            upper,lower = interval_set[(interval_set.index.hour==hour) & (interval_set.index.month==month)].iloc[0].values
            points = testset.loc[(testset.index.hour==hour) & (testset.index.month==month)]
            total += len(points)
            correct += points['Temperature'].between(lower,upper).sum()
    return correct/total


# In[9]:


def get_optimal(conf):
    optimal = pd.DataFrame()
    for month in range(1,13):
        for hour in range(24):
            points = testset[(testset.index.month==month) & (testset.index.hour==hour)]
            upper = points['Temperature'].quantile(conf)
            lower = points['Temperature'].quantile(1-conf)
            optimal = optimal.append({'Lower':lower,'Higher':upper},ignore_index=True)
    return optimal


# In[10]:


def get_width(interval):
    return (interval['Higher']-interval['Lower']).mean()


# In[11]:


conf = [0.8,0.9,0.95,0.99,1]


# In[12]:


optimal_line = pd.DataFrame()
for con in conf:
    optimal_line = optimal_line.append({'Confidence':con,'Width':get_width(get_optimal(con))},ignore_index=True)


# In[13]:


hist_points = pd.DataFrame()
for con in conf:
    intervals = get_historical(con,10)
    width = get_width(intervals)
    true_confidence = result(intervals)
    hist_points = hist_points.append({'Type':'Hist {}'.format(con),'Confidence':true_confidence,'Width':width,'Method':'Historical interval 10y'}, ignore_index=True)
for con in conf:
    intervals = get_historical(con,5)
    width = get_width(intervals)
    true_confidence = result(intervals)
    hist_points = hist_points.append({'Type':'Hist {}'.format(con),'Confidence':true_confidence,'Width':width,'Method':'Historical interval 5y'}, ignore_index=True)
for con in conf:
    intervals = get_historical(con,3)
    width = get_width(intervals)
    true_confidence = result(intervals)
    hist_points = hist_points.append({'Type':'Hist {}'.format(con),'Confidence':true_confidence,'Width':width,'Method':'Historical interval 3y'}, ignore_index=True)
for con in conf:
    intervals = get_historical(con,1)
    width = get_width(intervals)
    true_confidence = result(intervals)
    hist_points = hist_points.append({'Type':'Hist {}'.format(con),'Confidence':true_confidence,'Width':width,'Method':'Historical interval 1y'}, ignore_index=True)    


# In[23]:


def historical_boot(conf,year):    
    historic_interval = pd.DataFrame()
    historic_data = data
    historic_data.dt = pd.DatetimeIndex(historic_data.dt)
    historic_data = temp[(temp.index.year>2019-year) & (temp.index.year<2020)]
    for month in range(1,13):
        for hour in range(24):
                points = historic_data.loc[(historic_data.index.hour==hour) & (historic_data.index.month==month)]
                points = points['Temperature']
                points_size = len(points)
                higher_b,lower_b = [],[]
                for i in range(1000):
                    points_res = resample(points, replace=True, n_samples=points_size, random_state=1)
                    lower_b.append(points_res.quantile((1-conf)/2))
                    higher_b.append(points_res.quantile(1-(1-conf)/2))
                historic_interval = historic_interval.append({'Lower':np.mean(lower_b),'Higher':np.mean(higher_b)}, ignore_index=True)
    historic_interval = historic_interval.set_index(date)
    return historic_interval


# In[24]:


def historical_par_boot(conf,year):    
    historic_interval = pd.DataFrame()
    historic_data = data
    historic_data.dt = pd.DatetimeIndex(historic_data.dt)
    historic_data = temp[(temp.index.year>2019-year) & (temp.index.year<2020)]
    for month in range(1,13):
        for hour in range(24):
                points = historic_data.loc[(historic_data.index.hour==hour) & (historic_data.index.month==month)]
                points = points['Temperature']
                num_points = len(points)
                higher_b,lower_b = [],[]
                for i in range(1000):
                    boot_points = np.random.normal(points.mean(),points.std(), num_points)
                    points_res = resample(boot_points, replace=True, n_samples=num_points, random_state=1)
                    higher_b.append(np.quantile(points_res,(1-conf)/2))
                    lower_b.append(np.quantile(points_res,1-((1-conf)/2)))
                historic_interval = historic_interval.append({'Lower':np.mean(lower_b),'Higher':np.mean(higher_b)}, ignore_index=True)
    historic_interval = historic_interval.set_index(date)
    return historic_interval


# In[16]:


for con in conf:
    intervals = historical_boot(con,5)
    width = get_width(intervals)
    true_confidence = result(intervals)
    hist_points = hist_points.append({'Type':'Hist {}'.format(con),'Confidence':true_confidence,'Width':width,'Method':'5y bootstrap'}, ignore_index=True)  


# In[17]:


for con in conf:
    intervals = historical_par_boot(con,5)
    width = get_width(intervals)
    true_confidence = result(intervals)
    hist_points = hist_points.append({'Type':'Hist {}'.format(con),'Confidence':true_confidence,'Width':width,'Method':'5y bootstrap param'}, ignore_index=True)  


# In[25]:


for con in conf:
    intervals = historical_boot(con,10)
    width = get_width(intervals)
    true_confidence = result(intervals)
    hist_points = hist_points.append({'Type':'Hist {}'.format(con),'Confidence':true_confidence,'Width':width,'Method':'10y bootstrap'}, ignore_index=True)  


# In[26]:


for con in conf:
    intervals = historical_par_boot(con,10)
    width = get_width(intervals)
    true_confidence = result(intervals)
    hist_points = hist_points.append({'Type':'Hist {}'.format(con),'Confidence':true_confidence,'Width':width,'Method':'10y bootstrap param'}, ignore_index=True)  


# In[27]:


fg = sns.FacetGrid(data=hist_points, palette=sns.color_palette(),hue='Method', size=5, aspect=1.5)
fg.map(plt.scatter,'Confidence', 'Width').add_legend()
fg.axes[0,0].plot(optimal_line.Confidence, optimal_line['Width'], marker="o", label='Optimal')
plt.title("{} 2020".format(city))
plt.xlim(0.50, 1.01)
plt.savefig('output_dir/{}.png'.format(city))
hist_points.to_csv('output_dir/{}.csv'.format(city))


# In[ ]:




