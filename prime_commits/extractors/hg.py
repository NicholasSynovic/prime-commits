import logging
from datetime import datetime
from typing import List, Tuple

import hglib
import pandas
from hglib.client import hgclient
from pandas import DataFrame
from progress.bar import Bar

from prime_commits.sclc import cloc, scc
from prime_commits.utils import compute, filesystem
from prime_commits.utils.config import Config
from prime_commits.utils.types.hgCommitInformation import HgCommitInformation
from prime_commits.vcs import hg


def main(config: Config) -> None:
    if filesystem.checkIfHGRepository(path=config.PATH) == False:
        exit(1)
    repo: hgclient = hglib.open(path=config.PATH.__str__())

    if config.BRANCH is None:
        config.BRANCH: str = hg.getDefaultBranchName(repo=repo)

    if hg.checkIfBranch(branch=config.BRANCH, repo=repo) == False:
        exit(2)
    else:
        logging.info(msg=f"Using the {config.BRANCH} branch of {config.PATH}")

    hg.restoreRepoToBranch(branch=config.BRANCH, repo=repo)
    commitIterator: List[
        Tuple[bytes, bytes, bytes, bytes, bytes, bytes, datetime]
    ] = hg.getCommitIterator(branch=config.BRANCH, repo=repo)
    commitCount: int = hg.getCommitCount(commitIterator=commitIterator)

    with Bar("Extracting commit information...", max=commitCount) as bar:
        commit: Tuple[bytes, bytes, bytes, bytes, bytes, bytes, datetime]
        for commit in commitIterator:
            information: HgCommitInformation = HgCommitInformation(commit=commit)
            config.DF_LIST.append(information.__pd__())
            bar.next()

    df: DataFrame = pandas.concat(objs=config.DF_LIST, ignore_index=True).sort_values(
        by=["CommitDate"]
    )

    compute.computeDaysSince0(
        df=df, dateColumn="CommitDate", daysSince0_Column="CommitDaysSince0"
    )
    compute.computeDaysSince0(
        df=df, dateColumn="CommiterDate", daysSince0_Column="CommiterDaysSince0"
    )
    compute.computeDaysSince0(
        df=df, dateColumn="AuthorDate", daysSince0_Column="AuthorDaysSince0"
    )

    with Bar("Counting lines of code...", max=df.shape[0]) as bar:
        idx: int
        for idx in range(len(df)):
            hg.checkoutCommit(commitID=df["id"].iloc[idx])

            if config.SCLC == 0:
                sclcDF: DataFrame = scc.countLines()
            else:
                sclcDF: DataFrame = cloc.countLines(directory=config.PATH)

            updateDataFrameRowFromSCLC(df=df, sclcDF=sclcDF, dfIDX=idx)
            bar.next()
