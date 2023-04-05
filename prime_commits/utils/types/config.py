import logging
from argparse import Namespace
from pathlib import Path
from typing import List

from pandas import DataFrame
from pygit2 import Repository

from prime_commits.utils import filesystem


class Config:
    def __init__(self, args: Namespace) -> None:
        self.PATH: Path = args.directory
        self.BRANCH: str | None = args.gitBranch
        self.OUTPUT: Path = args.output
        self.LOG: Path = args.log
        self.PWD: Path = filesystem.getCWD()
        self.DF_LIST: List[DataFrame] = []

        self.REPO: Repository = Repository(path=self.PATH)

        logging.basicConfig(
            filename=self.LOG,
            format="%(asctime)s %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.INFO,
        )

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

        logging.info(msg=f"Parent working directory is: {self.PWD}")

        filesystem.switchDirectories(path=self.PATH)
        logging.info(msg=f"Now working in: {self.PATH}")
