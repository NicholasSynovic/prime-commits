import subprocess
from io import StringIO
from pathlib import Path
from subprocess import CompletedProcess

import pandas
from pandas import DataFrame

from prime_commits.utils.types.sclcInformation import SCLCInformation


def countLines(directory: Path) -> DataFrame:
    cmdStr: str = f"cloc --no-autogen --follow-links --skip-archive='(zip|tar(.(gz|Z|bz2|xz|7z))?)' --quiet --hide-rate --csv {directory.resolve().__str__()}"
    process: CompletedProcess = subprocess.run(
        args=cmdStr, stdout=subprocess.PIPE, shell=True
    )

    csv: StringIO = StringIO(process.stdout.decode())

    df: DataFrame = (
        pandas.read_csv(filepath_or_buffer=csv, header=0)
        .iloc[-1:]
        .reset_index(drop=True)
    )
    df.columns = df.columns.str.title()
    df["Lines"] = df.iloc[:, 2:5].sum(axis=1)

    sclc: SCLCInformation = SCLCInformation.convert(df=df)

    return sclc.df
