from datetime import datetime
from typing import List, Tuple

import pandas
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pandas import DataFrame
from progress.bar import Bar

from prime_commits.sclc import cloc, scc
from prime_commits.utils import compute, filesystem
from prime_commits.utils.config import Config
from prime_commits.utils.types.hgCommitInformation import HgCommitInformation
from prime_commits.utils.types.jsonSchema import schema
from prime_commits.vcs.hg import Hg


def main(config: Config) -> None:
    if filesystem.checkIfHGRepository(path=config.PATH, config=config) == False:
        exit(1)

    hg: Hg = Hg(repositoryPath=config.PATH, config=config)

    if config.BRANCH is None:
        config.BRANCH: str = hg.getDefaultBranchName()

    if hg.checkIfBranch(branch=config.BRANCH) == False:
        exit(2)
    else:
        config.LOGGER.info(msg=f"Using the {config.BRANCH} branch of {config.PATH}")

    hg.restoreRepoToBranch(branch=config.BRANCH)

    commitIterator: List[
        Tuple[bytes, bytes, bytes, bytes, bytes, bytes, datetime]
    ] = hg.getCommitIterator(branch=config.BRANCH)

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

            compute.updateDataFrameRowFromSCLC(df=df, sclcDF=sclcDF, dfIDX=idx)
            bar.next()

    hg.restoreRepoToBranch(branch=config.BRANCH)

    compute.computeDeltas(df=df, columnName="LOC", deltaColumnName="DLOC")
    compute.computeDeltas(df=df, columnName="KLOC", deltaColumnName="DKLOC")
    config.LOGGER.info(msg="Finished extracting commits")

    filesystem.switchDirectories(path=config.PWD, config=config)

    try:
        validate(instance=df.T.to_json(), schema=schema)
    except ValidationError:
        print(
            "\n",
            "ERROR: Unable to validate commits. Please see the log for more information",
        )
        config.LOGGER.info(
            msg=f"ERROR: Unable to validate JSON: {information.__dict__}"
        )
        exit(3)

    df.T.to_json(
        path_or_buf=config.OUTPUT,
        indent=4,
    )
    config.LOGGER.info(msg=f"Saved data to: {config.OUTPUT}")
