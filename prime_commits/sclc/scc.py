import subprocess
from subprocess import CompletedProcess

import pandas
from pandas import DataFrame

from prime_commits.utils.types.sclcInformation import SCLCInformation


def countLines() -> DataFrame:
    cmdStr: str = (
        "scc --format html-table --no-cocomo --no-complexity --no-duplicates --no-size"
    )
    process: CompletedProcess = subprocess.run(
        args=cmdStr, stdout=subprocess.PIPE, shell=True
    )

    df: DataFrame = (
        pandas.read_html(io=process.stdout, header=0)[0]
        .iloc[-1:]
        .reset_index(drop=True)
    )

    sclc: SCLCInformation = SCLCInformation.convert(df=df)

    return sclc.df
