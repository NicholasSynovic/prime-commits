import logging
from argparse import Namespace
from datetime import datetime
from pathlib import Path
from sys import exit
from typing import List
from warnings import filterwarnings

import pandas
from pandas import DataFrame, Series
from progress.bar import Bar
from pygit2 import Commit, Repository
from pygit2._pygit2 import Walker

from prime_commits.args.extractorArgs import getArgs
from prime_commits.sclc import scc
from prime_commits.utils import filesystem
from prime_commits.utils.types.commitInformation import CommitInformation
from prime_commits.vcs import git

filterwarnings(action="ignore")


def computeDaysSince0(df: DataFrame, dateColumn: str, daysSince0_Column: str) -> None:
    day0: int = datetime.fromtimestamp(df[dateColumn][0])
    df[daysSince0_Column] = df[dateColumn].apply(datetime.fromtimestamp) - day0
    df[daysSince0_Column] = pandas.to_timedelta(df[daysSince0_Column]).dt.days


def updateDataFrameRowFromSCC(df: DataFrame, sccDF: DataFrame, dfIDX: int) -> None:
    sccFiles: int = sccDF.loc[0, "Files"]
    sccLines: int = sccDF.loc[0, "Lines"]
    sccBlank: int = sccDF.loc[0, "Blank"]
    sccComment: int = sccDF.loc[0, "Comment"]
    sccCode: int = sccDF.loc[0, "Code"]
    sccComplexity: int = sccDF.loc[0, "Complexity"]
    sccBytes: int = sccDF.loc[0, "Bytes"]

    df["NumberOfFiles"].iloc[dfIDX] = sccFiles
    df["NumberOfLines"].iloc[dfIDX] = sccLines
    df["NumberOfBlankLines"].iloc[dfIDX] = sccBlank
    df["NumberOfCommentLines"].iloc[dfIDX] = sccComment
    df["LOC"].iloc[dfIDX] = sccCode
    df["KLOC"].iloc[dfIDX] = sccCode / 1000
    df["SCC_Complexity"].iloc[dfIDX] = sccComplexity
    df["Bytes"].iloc[dfIDX] = sccBytes


def computeDeltas(df: DataFrame, columnName: str, deltaColumnName: str) -> None:
    shift: Series = df[columnName].shift(periods=1, fill_value=0)
    df[deltaColumnName] = df[columnName] - shift


def main(args: Namespace) -> None:
    PATH: Path = args.directory
    BRANCH: str | None = args.branch
    OUTPUT: Path = args.output
    LOG: Path = args.log

    dfList: List[DataFrame] = []

    logging.basicConfig(
        filename=LOG,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )

    pwd: Path = filesystem.getCWD()
    logging.info(msg=f"Parent working directory is: {pwd}")

    filesystem.switchDirectories(path=PATH)
    logging.info(msg=f"Now working in: {PATH}")

    repo: Repository = Repository(path=PATH)

    if BRANCH is None:
        BRANCH: str = git.getHEADName_CMDLINE()

    if git.checkIfBranch(branch=BRANCH, repo=repo) is False:
        print(f"Invalid branch name ({BRANCH}) for repository: {PATH}")
        exit(3)

    logging.info(msg=f"Using the {BRANCH} branch of {PATH}")

    git.resetHEAD_CMDLINE(branch=BRANCH)
    commitWalker: Walker = git.getCommitWalker(repo=repo)
    commitCount: int = git.getCommitCount_CMDLINE()

    with Bar("Extracting commit information...", max=commitCount) as bar:
        commit: Commit
        while True:
            try:
                information: CommitInformation = CommitInformation(
                    commit=next(commitWalker)
                )
                dfList.append(information.__pd__())
                bar.next()
            except StopIteration:
                break

    df: DataFrame = pandas.concat(objs=dfList, ignore_index=True)

    computeDaysSince0(
        df=df, dateColumn="CommitDate", daysSince0_Column="CommitDaysSince0"
    )
    computeDaysSince0(
        df=df, dateColumn="CommiterDate", daysSince0_Column="CommiterDaysSince0"
    )
    computeDaysSince0(
        df=df, dateColumn="AuthorDate", daysSince0_Column="AuthorDaysSince0"
    )

    # TODO: Optimize DataFrame iteration. Vectorization?
    # TODO: Figure out how to optimally interface with a git repo. FUSE?
    with Bar("Counting lines of code...", max=len(df["id"])) as bar:
        idx: int
        for idx in range(len(df)):
            git.checkoutCommit_CMDLINE(commitID=df["id"].iloc[idx])
            sccDF: DataFrame = scc.countLines()
            updateDataFrameRowFromSCC(df=df, sccDF=sccDF, dfIDX=idx)
            bar.next()

    git.resetHEAD_CMDLINE(branch=BRANCH)
    logging.info(msg=f"Reset {PATH} to HEAD branch")

    computeDeltas(df=df, columnName="LOC", deltaColumnName="DLOC")
    computeDeltas(df=df, columnName="KLOC", deltaColumnName="DKLOC")
    logging.info(msg="Finished extracting commits")

    filesystem.switchDirectories(path=pwd)
    logging.info(msg=f"Now working in: {pwd}")

    df.T.to_json(
        path_or_buf=OUTPUT,
        indent=4,
    )
    logging.info(msg=f"Saved data to: {OUTPUT}")


if __name__ == "__main__":
    try:
        args: Namespace = getArgs()
    except KeyboardInterrupt:
        exit(1)

    try:
        main(args=args)
    except KeyboardInterrupt:
        pwd: Path = filesystem.getCWD()
        filesystem.switchDirectories(path=args.directory)
        git.resetHEAD_CMDLINE(branch=args.branch)
        filesystem.switchDirectories(path=pwd)
        exit(2)
