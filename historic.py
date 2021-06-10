import pandas as pd
import numpy as np
import cityRemap
from pathlib import Path

def get_historic(city, UTC_time, month, conf):
    try:
        if(city in cityRemap.high):
            data = pd.read_csv(Path('extracted\high\{}.csv'.format(city)))
        else:
            data = pd.read_csv(Path('extracted\owm\{}.csv'.format(city)))
    except:
        print("No city {}".format(city))

    data.dt = pd.DatetimeIndex(data.dt)
    points = data.loc[(data['dt'].dt.hour==UTC_time) & (data.dt.dt.month==month)]
    if(conf=='mean'):
        return np.mean(points)
    lower = points['Temperature'].quantile(round((1-conf)/2,3))
    higher = points['Temperature'].quantile(round(1-(1-conf)/2,3))
    return [lower,higher]
