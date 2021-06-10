import os
from pathlib import Path
import pandas as pd
import cityRemap

if not os.path.isdir('extracted'):
        os.makedirs(Path('extracted/low/'))
        os.makedirs(Path('extracted/high/'))
        os.makedirs(Path('extracted/combined/'))
        os.makedirs(Path('extracted/owm/'))

def clean_mtb(data,i):
    city = data.iloc[:,[i]].columns[0]
    city_cols = [col for col in data.columns if city in col]
    city_data = data[city_cols].iloc[3:]
    city_name = city_data.columns[0]
    city_data.columns = city_data.iloc[0] + " " + city_data.iloc[2]
    city_data = city_data.iloc[6:]
    city_data = city_data.astype(float)
    city_data.index = pd.to_datetime(city_data.index)
    return city_data,city_name

def extract_city(i,high,low):
    high_city,city_name = clean_mtb(high,i)
    low_city,city_name = clean_mtb(low,i)

    high_city = high_city.rename({'Temperature sfc':'Temperature','temp':'Temperature'},axis='columns')
    low_city = low_city.rename({'Temperature sfc':'Temperature','temp':'Temperature'},axis='columns')
    if ('Temperature' not in high_city.columns):
        high_city = high_city.rename({'Temperature 2 m elevation corrected':'Temperature'},axis='columns')
        low_city = low_city.rename({'Temperature 2 m elevation corrected':'Temperature'},axis='columns')
    high_city.index.names = ['dt']
    low_city.index.names = ['dt']
    high_city = high_city[pd.notnull(high_city['Temperature'])]
    low_city = low_city[pd.notnull(low_city['Temperature'])]

    high_city.to_csv(Path('extracted/high/{}.csv'.format(cityRemap.remaped.get(city_name))))
    low_city.to_csv(Path('extracted/low/{}.csv'.format(cityRemap.remaped.get(city_name))))

    for i in high_city:
        new = high_city[i].dropna()
        low_city[i].loc[new.index] = new

    low_city.to_csv(Path('extracted/combined/{}.csv'.format(cityRemap.remaped.get(city_name))))

#extract basic meteoblue
high_bsl = pd.read_csv('Materials/MeteoBlue_basic-weather-variables-only/dataexport_20210403T181231_hi-res_bsl.csv', low_memory=False)
low_bsl = pd.read_csv('Materials/MeteoBlue_basic-weather-variables-only/dataexport_20210403T181428_lo-res_bsl.csv', low_memory=False)

high_bsl = high_bsl.set_index('location');
low_bsl = low_bsl.set_index('location');

high_bsl.rename({'Temperature 2 m elevation corrected':'Temperature'},axis='columns')
low_bsl.rename({'Temperature 2 m elevation corrected':'Temperature'},axis='columns')

extract_city(0,high_bsl,low_bsl)

#extract complete meteoblue
high = pd.read_csv("Materials/MeteoBlue_all-variables-incl-radiation/dataexport_20210422T200404_all-vars_hi-res.csv", low_memory=False)
low = pd.read_csv("Materials/MeteoBlue_all-variables-incl-radiation/dataexport_20210422T202657_all-vars_lo-res.csv", low_memory=False)
high = high.set_index('location');
low = low.set_index('location');

for i in range(10):
    extract_city(i,high,low)

#extract openweathermap
from glob import glob
PATH = "Materials/OpenWeatherMap/"
EXT = "*.csv"
all_csv_files = [file
                 for path, subdir, files in os.walk(PATH)
                 for file in glob(os.path.join(path, EXT))]
for file in all_csv_files:
    city = pd.read_csv(file)
    city.dt = city.dt.astype('datetime64[s]')
    city = city.set_index('dt')
    city_name = city['city_name'][0]
    city = city.drop(columns=['lat','lon','weather_icon','dt_iso','timezone','city_name','weather_id','weather_main','weather_description'])
    city.rename({'temp':'Temperature'})
    city.to_csv(Path('extracted/owm/{}.csv'.format(cityRemap.remaped.get(city_name))))