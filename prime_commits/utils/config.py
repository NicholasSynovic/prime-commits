import logging
from argparse import Namespace
from logging import FileHandler, Formatter, Logger
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
        self.DF_LIST: List[DataFrame] = []
        self.LOGGER = Logger(name="PRIME Commit Extractor", level=logging.INFO)

        logFileHandler: FileHandler = FileHandler(filename=self.LOG)
        logDateFormat: Formatter = Formatter(
            fmt="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        logFileHandler.setFormatter(fmt=logDateFormat)
        self.LOGGER.addHandler(hdlr=logFileHandler)

        self.PWD: Path = filesystem.getCWD(config=self)

        if filesystem.checkIfValidDirectoryPath(path=self.PATH, config=self) == False:
            exit(1)

        self.SCLC: int
        match args.sclc:
            case "scc":
                self.SCLC = 0
                self.LOGGER.info(msg=f"Using SCC as SCLC")
            case "cloc":
                self.SCLC = 1
                self.LOGGER.info(msg=f"Using CLOC as SCLC")
            case _:
                exit(1)

        self.LOGGER.info(msg=f"Parent working directory is {self.PWD}")

        filesystem.switchDirectories(path=self.PATH, config=self)
