from itertools import pairwise
from pathlib import PurePath
from time import time
from typing import List

import pandas
from pandas import DataFrame
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


def main() -> None:
    dfList: List[DataFrame] = []
    pwd: PurePath = filesystem.getCWD()

    filesystem.switchDirectories(path=PATH)
    repo: Repository = Repository(path=PATH)

    commitWalker: Walker = git.getCommitWalker(repo=repo)

    print("Getting commit count (Takes a while...)")
    commitCount: int = git.getCommitCount_CMDLINE()

    with Bar("Extracting commit information...", max=commitCount) as bar:
        commit: Commit
        for commit in commitWalker:
            information: CommitInformation = CommitInformation(commit=commit)
            dfList.append(information.__pd__())
            bar.next()

    print("Concatinating DFs...")
    df: DataFrame = pandas.concat(objs=dfList, ignore_index=True)

    for id in df["id"]:
        git.checkoutCommit_CMDLINE(commitID=id)
        scc.countLines()
        quit()

    git.exitDetachedHEAD_CMDLINE(branch="main")

    print(filesystem.getCWD())
    # print(df)

    # commitIDPairs: pairwise = pairwise(df["id"])

    # commitPairs: pairwise = createCommitPairing(commits=commitWalker)

    # args: Namespace = mainArgs()

    # directory: PurePath = PurePath(args.directory)
    # directoryChecks: filesystemChecks = testPath(path=directory)


if __name__ == "__main__":
    main()
