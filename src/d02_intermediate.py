import d01_data as da

import pandas as pd
import datetime as dt
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar


def getseverity(col1, col2):
    return pd.concat([(col1>0)*2, (col2>0)*1], axis=1).max(axis=1)   

def cleandata(df):
    temp = df['CRASH DATE'] + ' '+ df['CRASH TIME']
    df = df.drop(['CRASH DATE', 'CRASH TIME'], axis=1)
    df['DATE'] = pd.to_datetime(temp, format="%m/%d/%Y %H:%M")
    
    #Return the day of the week as an integer, where Monday is 1 and Sunday is 7.
    df['WEEKDAY'] = df['DATE'].dt.weekday + 1
    df['YEAR'] = df['DATE'].dt.year
    df['MONTH'] = df['DATE'].dt.month
    df['DAY'] = df['DATE'].dt.day
    df['HOUR'] = df['DATE'].dt.hour
    df['MINUTE'] = df['DATE'].dt.minute
    
    #Exclude "cut" years 2012 and 2020 (2020 might be biased due to Coronavirus anyway)
    df = df[~df['YEAR'].isin([2012, 2020])]
    
    #Define Holiday Column
    cal = calendar()
    holidays = cal.holidays(start=df['DATE'].min(), end=df['DATE'].max())
    df['HOLIDAY'] = df['DATE'].isin(holidays)
    
    #Boroughs
    df['BOROUGH'] = df['BOROUGH'].fillna('UNKNOWN')
    
    #ZIP Codes
    df['ZIP CODE'] = df['ZIP CODE'].fillna('0')
    df['ZIP CODE'].replace(to_replace='     ', value='0', inplace=True)
    df['ZIP CODE'] = df['ZIP CODE'].astype('int64').astype('str')
    df['ZIP CODE'].replace(to_replace='     ', value='00000', inplace=True)
    df['ZIP CODE'].replace(to_replace='0', value='00000', inplace=True)
    
    #GPS Data and Location
    df[['LATITUDE', 'LONGITUDE']] = df[['LATITUDE', 'LONGITUDE']].fillna(0.)
    df['LOCATION'] = df['LOCATION'].fillna('UNKNOWN')
    
    #Drop Street Info
    df = df.drop(['ON STREET NAME', 'CROSS STREET NAME', 'OFF STREET NAME'], axis=1)
    
    #Injuries and Fatalities Numbers
    temp_inj = df['NUMBER OF PEDESTRIANS INJURED']+df['NUMBER OF CYCLIST INJURED']+df['NUMBER OF MOTORIST INJURED']
    temp_kll = df['NUMBER OF PEDESTRIANS KILLED']+df['NUMBER OF CYCLIST KILLED']+df['NUMBER OF MOTORIST KILLED']
    df['NUMBER OF PERSONS INJURED'] = df['NUMBER OF PERSONS INJURED'].fillna(temp_inj)
    df['NUMBER OF PERSONS KILLED'] = df['NUMBER OF PERSONS KILLED'].fillna(temp_kll)
    ##Remove inconsistent accidents (data errors)
    df = df.drop(df[(df['NUMBER OF PERSONS KILLED']!=temp_kll) & (df['NUMBER OF PERSONS INJURED']!=temp_inj)].index)
    df[['NUMBER OF PERSONS INJURED', 
        'NUMBER OF PERSONS KILLED', 
        'NUMBER OF PEDESTRIANS INJURED', 
        'NUMBER OF PEDESTRIANS KILLED', 
        'NUMBER OF CYCLIST INJURED', 
        'NUMBER OF CYCLIST KILLED', 
        'NUMBER OF MOTORIST INJURED', 
        'NUMBER OF MOTORIST KILLED']] =\
    df[['NUMBER OF PERSONS INJURED', 
        'NUMBER OF PERSONS KILLED', 
        'NUMBER OF PEDESTRIANS INJURED', 
        'NUMBER OF PEDESTRIANS KILLED', 
        'NUMBER OF CYCLIST INJURED', 
        'NUMBER OF CYCLIST KILLED', 
        'NUMBER OF MOTORIST INJURED', 
        'NUMBER OF MOTORIST KILLED']].astype('int32')
    
    #Collision ID
    df = df.drop(['COLLISION_ID'], axis=1)
    
    #Contributing Factor Vehicles
    df[['CONTRIBUTING FACTOR VEHICLE 1', 
        'CONTRIBUTING FACTOR VEHICLE 2', 
        'CONTRIBUTING FACTOR VEHICLE 3', 
        'CONTRIBUTING FACTOR VEHICLE 4', 
        'CONTRIBUTING FACTOR VEHICLE 5',
        'VEHICLE TYPE CODE 1', 
        'VEHICLE TYPE CODE 2', 
        'VEHICLE TYPE CODE 3', 
        'VEHICLE TYPE CODE 4', 
        'VEHICLE TYPE CODE 5']] =\
    df[['CONTRIBUTING FACTOR VEHICLE 1', 
        'CONTRIBUTING FACTOR VEHICLE 2', 
        'CONTRIBUTING FACTOR VEHICLE 3', 
        'CONTRIBUTING FACTOR VEHICLE 4', 
        'CONTRIBUTING FACTOR VEHICLE 5',
        'VEHICLE TYPE CODE 1', 
        'VEHICLE TYPE CODE 2', 
        'VEHICLE TYPE CODE 3', 
        'VEHICLE TYPE CODE 4', 
        'VEHICLE TYPE CODE 5']].replace(to_replace='Unspecified', value='None').fillna('None')
    
    #Severity
    df['SEVERITY'] = getseverity(df['NUMBER OF PERSONS KILLED'], df['NUMBER OF PERSONS INJURED'])
    
    #Rearrange Data
    df = df[['DATE', 
     'YEAR', 
     'MONTH',
     'DAY',
     'HOUR',
     'MINUTE',
     'WEEKDAY',
     'HOLIDAY',
     'BOROUGH',
     'ZIP CODE',
     'LATITUDE',
     'LONGITUDE',
     'LOCATION',
     'SEVERITY',
     'NUMBER OF PERSONS INJURED',
     'NUMBER OF PERSONS KILLED',
     'NUMBER OF PEDESTRIANS INJURED',
     'NUMBER OF PEDESTRIANS KILLED',
     'NUMBER OF CYCLIST INJURED',
     'NUMBER OF CYCLIST KILLED',
     'NUMBER OF MOTORIST INJURED',
     'NUMBER OF MOTORIST KILLED',
     'CONTRIBUTING FACTOR VEHICLE 1',
     'CONTRIBUTING FACTOR VEHICLE 2',
     'CONTRIBUTING FACTOR VEHICLE 3',
     'CONTRIBUTING FACTOR VEHICLE 4',
     'CONTRIBUTING FACTOR VEHICLE 5',
     'VEHICLE TYPE CODE 1',
     'VEHICLE TYPE CODE 2',
     'VEHICLE TYPE CODE 3',
     'VEHICLE TYPE CODE 4',
     'VEHICLE TYPE CODE 5']]
    
    df = df.sort_values(by=['DATE'])
    return df


def main():
    df = pd.read_csv(r'..\data\01_raw\Motor_Vehicle_Collisions_-_Crashes.csv')
    df = cleandata(df)
    da.exportdatatofeather(df, r'..\data\02_intermediate\NYC_VehicleCollisions_cleaned.feather')
    
main()
    