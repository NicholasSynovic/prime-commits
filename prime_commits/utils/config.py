import logging
from argparse import Namespace
from pathlib import Path
from typing import List

from pandas import DataFrame

from prime_commits.utils import filesystem


class Config:
    def __init__(self, args: Namespace) -> None:
        self.PATH: Path = args.directory.resolve()
        self.BRANCH: str | None = args.branch
        self.OUTPUT: Path = args.output.resolve()
        self.LOG: Path = args.log.resolve()
        self.PWD: Path = filesystem.getCWD()
        self.DF_LIST: List[DataFrame] = []

        if filesystem.checkIfValidDirectoryPath(path=self.PATH) == False:
            exit(1)

        self.SCLC: int
        match args.sclc:
            case "scc":
                self.SCLC = 0
                logging.info(msg=f"Using SCC as SCLC")
            case "cloc":
                self.SCLC = 1
                logging.info(msg=f"Using CLOC as SCLC")
            case _:
                exit(1)

        logging.info(msg=f"Parent working directory is {self.PWD}")

        filesystem.switchDirectories(path=self.PATH)
