from datetime import datetime

import pandas
from pandas import DataFrame, Series


def computeDaysSince0(df: DataFrame, dateColumn: str, daysSince0_Column: str) -> None:
    day0: int = datetime.fromtimestamp(df[dateColumn][0])
    df[daysSince0_Column] = df[dateColumn].apply(datetime.fromtimestamp) - day0
    df[daysSince0_Column] = pandas.to_timedelta(df[daysSince0_Column]).dt.days


def computeDeltas(df: DataFrame, columnName: str, deltaColumnName: str) -> None:
    shift: Series = df[columnName].shift(periods=1, fill_value=0)
    df[deltaColumnName] = df[columnName] - shift
