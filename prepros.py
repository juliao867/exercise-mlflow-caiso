import pandas as pd
from datetime import timedelta as td

def get_train_test(date=None):
    # Load the data
    df = pd.read_csv("data/power.csv")


     ###Parse timestamps and remove timezone
    df["time"] = pd.to_datetime(df["time"])
    df["time"] = df["time"].dt.tz_localize(None)
    df = df.set_index("time").sort_index()


    ###resample from minute interval to hourly intervals and change column name to mean
    df = df.resample("1h").mean()

    if "Total" in df.columns:
        df = df.rename(columns={"Total": "mean"})
    else:
        raise ValueError("CSV must contain a 'Total' column")

    ###Select last 22 days ending at date
    end_time = pd.to_datetime(date) if date else df.index.max()
    start_time = end_time - td(days=22)
    df = df.loc[start_time:end_time].dropna()

    ###Split last 24 hours → test, rest → train
    train = df.iloc[:-24]
    test  = df.iloc[-24:]

    train_x, train_y = split_labels(train)
    test_x, test_y = split_labels(test)
    return train_x, train_y, test_x, test_y


def split_labels(df):
    x = df.index.to_frame(index=False).rename(columns={"time": "Time"})
    y = df[["mean"]].rename(columns={"mean": "Demand"})
    x.index = y.index = range(len(df))
    return x, y
