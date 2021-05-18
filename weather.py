import os
import pandas as pd
import pickle
from pathlib import Path

def get_interval(UTC_time):
    pass
    

def get_historic(city, UTC_time, month, conf):
    #time 0-23 #month 1-12
    # MeteoBlue = pd.read_csv(Path('Materials/MeteoBlue_basic-weather-variables-only/dataexport_20210401T200237_lo-res.csv'))
    # city = MeteoBlue[['location','Amsterdam']][9:]
    # city['location'] = city['location'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%dT%H%M'))
    file = open('Extracted/{}.pk'.format(city),'rb')
    data = pickle.load(file)
    points = data.loc[(data.index.hour==UTC_time) & (data.index.month==month)]
    lower = points[city].quantile(round((1-conf)/2,3))
    higher = points[city].quantile(round(1-(1-conf)/2,3))
    return [lower,higher]

def extract_cities():
    if not os.path.isdir('Extracted'):
        os.mkdir('Extracted')
        cities = pd.read_csv('Materials/MeteoBlue_basic-weather-variables-only/dataexport_20210401T200237_lo-res.csv', index_col=0, nrows=0,low_memory=False).columns.tolist()
        cities = cities[0:int(len(cities)/4)]
        data = pd.read_csv('Materials/MeteoBlue_basic-weather-variables-only/dataexport_20210401T200237_lo-res.csv',low_memory=False)
        for city in cities:
            city_temp = data[['location',city]][9:]
            city_temp['location'] = city_temp['location'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%dT%H%M'))
            city_temp.rename(columns={'location':'time'}, inplace=True)
            city_temp.set_index('time', inplace=True)
            city_temp[city] = city_temp[city].astype(float)
            file = open(Path('Extracted/{}.pk'.format(city)),'wb')
            pickle.dump(city_temp,file)
        
extract_cities()

if __name__ == '__main__':
    get_historic(1,1,'Amsterdam',0.95)
