import pandas as pd


def exportdatatofeather(df, location, drop=True):
    df = df.reset_index(drop=drop)
    df.to_feather(location)
