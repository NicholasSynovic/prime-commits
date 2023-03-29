import subprocess
from subprocess import CompletedProcess

import pandas
from pandas import DataFrame


def countLines() -> DataFrame:
    cmdStr: str = "scc -f html-table"
    process: CompletedProcess = subprocess.run(
        args=cmdStr, stdout=subprocess.PIPE, shell=True
    )
    return pandas.read_html(io=process.stdout)[0]
