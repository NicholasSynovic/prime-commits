import logging
from argparse import Namespace
from datetime import datetime
from pathlib import Path
from typing import List
from warnings import filterwarnings

import pandas
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pandas import DataFrame, Series
from progress.bar import Bar
from pygit2 import Commit, Repository
from pygit2._pygit2 import Walker

from prime_commits.args.extractorArgs import getArgs
from prime_commits.sclc import cloc, scc
from prime_commits.utils import filesystem
from prime_commits.utils.types.commitInformation import CommitInformation
from prime_commits.utils.types.schema import schema
from prime_commits.vcs import git

filterwarnings(action="ignore")


def computeDaysSince0(df: DataFrame, dateColumn: str, daysSince0_Column: str) -> None:
    day0: int = datetime.fromtimestamp(df[dateColumn][0])
    df[daysSince0_Column] = df[dateColumn].apply(datetime.fromtimestamp) - day0
    df[daysSince0_Column] = pandas.to_timedelta(df[daysSince0_Column]).dt.days


def updateDataFrameRowFromSCC(df: DataFrame, sclcDF: DataFrame, dfIDX: int) -> None:
    sccFiles: int = sclcDF.loc[0, "Files"]
    sccLines: int = sclcDF.loc[0, "Lines"]
    sccBlank: int = sclcDF.loc[0, "Blank"]
    sccComment: int = sclcDF.loc[0, "Comment"]
    sccCode: int = sclcDF.loc[0, "Code"]

    df["NumberOfFiles"].iloc[dfIDX] = sccFiles
    df["NumberOfLines"].iloc[dfIDX] = sccLines
    df["NumberOfBlankLines"].iloc[dfIDX] = sccBlank
    df["NumberOfCommentLines"].iloc[dfIDX] = sccComment
    df["LOC"].iloc[dfIDX] = sccCode
    df["KLOC"].iloc[dfIDX] = sccCode / 1000


def computeDeltas(df: DataFrame, columnName: str, deltaColumnName: str) -> None:
    shift: Series = df[columnName].shift(periods=1, fill_value=0)
    df[deltaColumnName] = df[columnName] - shift


def main() -> None:
    args: Namespace = getArgs()

    PATH: Path = args.gitDirectory
    BRANCH: str | None = args.gitBranch
    OUTPUT: Path = args.gitOutput
    LOG: Path = args.gitLog

    logging.basicConfig(
        filename=LOG,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )

    SCLC: int
    if args.sclc == "scc":
        SCLC = 0
        logging.info(msg=f"Using SCC as SCLC")
    else:
        SCLC = 1
        logging.info(msg=f"Using CLOC as SCLC")

    dfList: List[DataFrame] = []

    pwd: Path = filesystem.getCWD()
    logging.info(msg=f"Parent working directory is: {pwd}")

    filesystem.switchDirectories(path=PATH)
    logging.info(msg=f"Now working in: {PATH}")

    repo: Repository = Repository(path=PATH)

    if BRANCH is None:
        BRANCH: str = git.getHEADName_CMDLINE()

    if git.checkIfBranch(branch=BRANCH, repo=repo) is False:
        print(f"Invalid branch name ({BRANCH}) for repository: {PATH}")
        exit(2)

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

    with Bar("Counting lines of code...", max=len(df["id"])) as bar:
        idx: int
        for idx in range(len(df)):
            git.checkoutCommit_CMDLINE(commitID=df["id"].iloc[idx])

            if SCLC == 0:
                sclcDF: DataFrame = scc.countLines()
            else:
                sclcDF: DataFrame = cloc.countLines(directory=PATH)

            updateDataFrameRowFromSCC(df=df, sclcDF=sclcDF, dfIDX=idx)
            bar.next()

    git.resetHEAD_CMDLINE(branch=BRANCH)
    logging.info(msg=f"Reset {PATH} to HEAD branch")

    computeDeltas(df=df, columnName="LOC", deltaColumnName="DLOC")
    computeDeltas(df=df, columnName="KLOC", deltaColumnName="DKLOC")
    logging.info(msg="Finished extracting commits")

    filesystem.switchDirectories(path=pwd)
    logging.info(msg=f"Now working in: {pwd}")

    try:
        validate(instance=df.T.to_json(), schema=schema)
    except ValidationError:
        print(
            "\n",
            "ERROR: Unable to validate commits. Please see the log for more information",
        )
        logging.info(msg=f"ERROR: Unable to validate JSON: {information.__dict__}")
        exit(3)

    df.T.to_json(
        path_or_buf=OUTPUT,
        indent=4,
    )
    logging.info(msg=f"Saved data to: {OUTPUT}")


if __name__ == "__main__":
    main()
