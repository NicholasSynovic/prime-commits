from itertools import pairwise
from time import time
from typing import List

import pandas
from pandas import DataFrame
from progress.bar import Bar
from pygit2 import Commit, Repository
from pygit2._pygit2 import Walker

from prime_commits.utils.types.commitInformation import CommitInformation
from prime_commits.vcs import git
from prime_commits.vcs.general import createCommitPairing


def main() -> None:
    dfList: List[DataFrame] = []
    pathStr: str = "/home/nsynovic/downloads/linux"

    repo: Repository = Repository(path=pathStr)

    commitWalker: Walker = git.getCommitWalker(repo=repo)

    print("Getting commit count (Takes a while...)")
    commitCount: int = git.getCommitCount_CMDLINE(repo=repo)

    with Bar("Extracting commit information...", max=commitCount) as bar:
        commit: Commit
        for commit in commitWalker:
            information: CommitInformation = CommitInformation(commit=commit)
            dfList.append(information.__pd__())
            bar.next()

    print("Concatinating DFs...")
    df: DataFrame = pandas.concat(objs=dfList, ignore_index=True)
    df.to_json("test.json")

    commitPairs: pairwise = createCommitPairing(commits=commitWalker)

    # args: Namespace = mainArgs()

    # directory: PurePath = PurePath(args.directory)
    # directoryChecks: filesystemChecks = testPath(path=directory)


if __name__ == "__main__":
    main()
