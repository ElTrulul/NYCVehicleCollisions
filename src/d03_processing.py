import pandas as pd
import d01_data as da


def groupbyhour(df, excludeholidays=False):
    if excludeholidays:
        df = df[~df.WEEKDAY.isin([6,7])]
        df = df[~df.HOLIDAY]
    dfhour = df.groupby(['HOUR']).agg({'DATE' : 'count'})
    dfhour = dfhour.rename(columns={'DATE': 'TOTAL CRASHS'})
    dfhour['DEADLY CRASHS'] = df[df['NUMBER OF PERSONS KILLED']>0].groupby('HOUR').count().DATE
    dfhour['DANGEROUS CRASHS'] = df[(df['NUMBER OF PERSONS KILLED']>0) | (df['NUMBER OF PERSONS INJURED']>0)].groupby('HOUR').count().DATE
    dfhour['DEATH RATE'] = dfhour['DEADLY CRASHS']/dfhour['TOTAL CRASHS']
    dfhour['DANGER RATE'] = dfhour['DANGEROUS CRASHS']/dfhour['TOTAL CRASHS']
    return dfhour

def groupdataframe(dataframe,by):
    df = dataframe.groupby(by).agg({
        'DATE' : 'count',
        'NUMBER OF PERSONS INJURED' : 'sum',
        'NUMBER OF PERSONS KILLED' : 'sum',
        'NUMBER OF PEDESTRIANS INJURED' : 'sum',
        'NUMBER OF PEDESTRIANS KILLED' : 'sum',
        'NUMBER OF CYCLIST INJURED' : 'sum',
        'NUMBER OF CYCLIST KILLED' : 'sum',
        'NUMBER OF MOTORIST INJURED' : 'sum',
        'NUMBER OF MOTORIST KILLED' : 'sum'})
    if len(by)>1:
        df = df.reset_index()
    df = df.rename(columns={'DATE' : 'TOTALS'})
    return df    

def main():
    #Read data
    df = pd.read_feather(r'..\data\02_intermediate\NYC_VehicleCollisions_cleaned.feather')
    #Group and Export data
    da.exportdatatofeather(groupdataframe(df, ['BOROUGH']), r'..\data\03_processed\NYC_proc_byborough.feather', drop=False)
    da.exportdatatofeather(groupdataframe(df, ['YEAR']), r'..\data\03_processed\NYC_proc_byyear.feather', drop=False)
    da.exportdatatofeather(groupdataframe(df, ['MONTH']), r'..\data\03_processed\NYC_proc_bymonth.feather', drop=False)
    da.exportdatatofeather(groupdataframe(df, ['WEEKDAY']), r'..\data\03_processed\NYC_proc_byweekday.feather', drop=False)
    da.exportdatatofeather(groupdataframe(df,['BOROUGH', 'YEAR']), r'..\data\03_processed\NYC_proc_byboroughyear.feather', drop=False)
    da.exportdatatofeather(groupdataframe(df, ['CONTRIBUTING FACTOR VEHICLE 1']), r'..\data\03_processed\NYC_proc_bycauses.feather', drop=False)
    da.exportdatatofeather(groupbyhour(df, excludeholidays=True), r'..\data\03_processed\NYC_proc_byhour.feather', drop=False)

main()