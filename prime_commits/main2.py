from itertools import pairwise
from pathlib import PurePath
from time import time
from typing import List

import pandas
from pandas import DataFrame, Series
from progress.bar import Bar
from pygit2 import Commit, Repository
from pygit2._pygit2 import Walker

from prime_commits.sclc import scc
from prime_commits.utils import filesystem
from prime_commits.utils.types.commitInformation import CommitInformation
from prime_commits.vcs import git
from prime_commits.vcs.general import createCommitPairing

PATH: PurePath = PurePath("/home/nsynovic/downloads/linux")
PATH = PurePath("/home/nsynovic/documents/projects/ssl/forks/asgard")


def updateDataFrameRowFromSCC(df: DataFrame, sccDF: DataFrame, dfIDX: int) -> None:
    df["NumberOfFiles"].iloc[dfIDX] = sccDF["Files"][0]
    df["NumberOfLines"].iloc[dfIDX] = sccDF["Lines"][0]
    df["NumberOfBlankLines"].iloc[dfIDX] = sccDF["Blank"][0]
    df["NumberOfCommentLines"].iloc[dfIDX] = sccDF["Comment"][0]
    df["LOC"].iloc[dfIDX] = sccDF["Code"][0]
    df["KLOC"].iloc[dfIDX] = sccDF["Code"][0] / 1000
    df["SCC_Complexity"].iloc[dfIDX] = sccDF["Complexity"][0]
    df["Bytes"].iloc[dfIDX] = sccDF["Bytes"][0]


def main() -> None:
    dfList: List[DataFrame] = []
    pwd: PurePath = filesystem.getCWD()

    filesystem.switchDirectories(path=PATH)
    git.resetHEAD_CMDLINE(branch="main")
    repo: Repository = Repository(path=PATH)
    commitWalker: Walker = git.getCommitWalker(repo=repo)

    commitCount: int = git.getCommitCount_CMDLINE()

    with Bar("Extracting commit information...", max=commitCount) as bar:
        commit: Commit
        for commit in commitWalker:
            information: CommitInformation = CommitInformation(commit=commit)
            dfList.append(information.__pd__())
            bar.next()

    df: DataFrame = pandas.concat(objs=dfList, ignore_index=True)

    # TODO: Optimize DataFrame iteration. Vecotrization?
    with Bar("Counting lines of code...", max=len(df["id"])) as bar:
        idx: int
        for idx in range(len(df)):
            git.checkoutCommit_CMDLINE(commitID=df["id"].iloc[idx])
            sccDF: DataFrame = scc.countLines()
            updateDataFrameRowFromSCC(df=df, sccDF=sccDF, dfIDX=idx)
            bar.next()

        git.resetHEAD_CMDLINE(branch="main")

    filesystem.switchDirectories(path=pwd)
    df.T.to_json(
        "test.json",
        indent=4,
    )


if __name__ == "__main__":
    main()
