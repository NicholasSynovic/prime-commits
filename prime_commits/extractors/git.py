import logging

import pandas
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pandas import DataFrame
from progress.bar import Bar
from pygit2._pygit2 import Walker

from prime_commits.sclc import cloc, scc
from prime_commits.utils import compute, filesystem
from prime_commits.utils.config import Config
from prime_commits.utils.types.gitCommitInformation import GitCommitInformation
from prime_commits.utils.types.jsonSchema import schema
from prime_commits.vcs.git import Git


def updateDataFrameRowFromSCLC(df: DataFrame, sclcDF: DataFrame, dfIDX: int) -> None:
    sclcFiles: int = sclcDF.loc[0, "Files"]
    sclcLines: int = sclcDF.loc[0, "Lines"]
    sclcBlank: int = sclcDF.loc[0, "Blank"]
    sclcComment: int = sclcDF.loc[0, "Comment"]
    sclcCode: int = sclcDF.loc[0, "Code"]

    df["NumberOfFiles"].iloc[dfIDX] = sclcFiles
    df["NumberOfLines"].iloc[dfIDX] = sclcLines
    df["NumberOfBlankLines"].iloc[dfIDX] = sclcBlank
    df["NumberOfCommentLines"].iloc[dfIDX] = sclcComment
    df["LOC"].iloc[dfIDX] = sclcCode
    df["KLOC"].iloc[dfIDX] = sclcCode / 1000


def main(config: Config) -> None:
    if filesystem.checkIfGitRepository(path=config.PATH) == False:
        exit(1)

    git: Git = Git(repositoryPath=config.PATH)

    if config.BRANCH is None:
        config.BRANCH: str = git.getDefaultBranchName()

    if git.checkIfBranch(branch=config.BRANCH) == False:
        exit(2)
    else:
        logging.info(msg=f"Using the {config.BRANCH} branch of {config.PATH}")

    git.restoreRepoToBranch(branch=config.BRANCH)

    commitIterator: Walker = git.getCommitIterator()
    commitCount: int = git.getCommitCount(branch=config.BRANCH)

    with Bar("Extracting commit information...", max=commitCount) as bar:
        while True:
            try:
                information: GitCommitInformation = GitCommitInformation(
                    commit=next(commitIterator)
                )
                config.DF_LIST.append(information.__pd__())
                bar.next()
            except StopIteration:
                break

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
            git.checkoutCommit(commitID=df["id"].iloc[idx])

            if config.SCLC == 0:
                sclcDF: DataFrame = scc.countLines()
            else:
                sclcDF: DataFrame = cloc.countLines(directory=config.PATH)

            updateDataFrameRowFromSCLC(df=df, sclcDF=sclcDF, dfIDX=idx)
            bar.next()

    git.restoreRepoToBranch(branch=config.BRANCH)

    compute.computeDeltas(df=df, columnName="LOC", deltaColumnName="DLOC")
    compute.computeDeltas(df=df, columnName="KLOC", deltaColumnName="DKLOC")
    logging.info(msg="Finished extracting commits")

    filesystem.switchDirectories(path=config.PWD)

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
        path_or_buf=config.OUTPUT,
        indent=4,
    )
    logging.info(msg=f"Saved data to: {config.OUTPUT}")
