import pandas as pd

remaped = {
    'Frankfurt':'FRA',
    'Frankfurt am Main':'FRA',
    'Basel':'BSL',
    'Amsterdam':'AMS',
    'Amsterdam Airport Schiphol':'AMS',
    'Brussels':'BRU',
    'Zurich':'ZRH',
    'Zurich Airport':'ZRH',
    'Dubai':'DXB',
    'Dubai International Airport':'DXB',
    'Hyderabad':'HYD',
    'Begumpet Airport':'HYD',
    'Shanghai Pu Dong':'PVG',
    'Shanghai Pudong International Airport':'PVG',
    'Singapore':'SIN',
    'Singapore Changi Airport':'SIN',
    'Hongkong':'HKG',
    'Hong Kong International Airport':'HKG',
    'Tokyo Narita':'NRT',
    'Narita International Airport':'NRT',
    'San Francisco':'SFO',
    'San Francisco International Airport':'SFO',
    'Chicago':'ORD',
    "Chicago O'Hare International Airport":'ORD',
    'Sydney':'SYD',
    'Sydney Airport':'SYD',
    'Santiogo de Chili':'SCL',
    'Comodoro Arturo Merino Benítez International Airport':'SCL',
    'Johannesburg':'JNB',
    'O.R. Tambo International Airport':'JNB',
    'Lima':'LIM',
    'Jorge Chávez International Airport':'LIM'
}

mtb = ['AMS','BRU','BSL','DXB','FRA','HYD','JNB','LIM','ORD','PVG','SCL']
owm = ['HKG','NRT','SFO','SIN','SYD','ZRH']

month = {
    0:'JAN',
    1:'FEB',
    2:'MAR',
    3:'APR',
    4:'MAY',
    5:'JUN',
    6:'JUL',
    7:'AUG',
    8:'SEP',
    9:'OCT',
    10:'NOV',
    11:'DEC'
}

date_index=pd.DataFrame()
for current_month in range(12):
    for hour in range(24):
        date_index = date_index.append({'Date':'{} {}'.format(month.get(current_month),hour)},ignore_index=True)