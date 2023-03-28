from itertools import pairwise
from typing import List

import pandas
from pandas import DataFrame
from progress.spinner import Spinner
from pygit2 import Commit, Repository
from pygit2._pygit2 import Walker

from prime_commits.utils.types.commitInformation import CommitInformation
from prime_commits.vcs import git
from prime_commits.vcs.general import createCommitPairing


def main() -> None:
    pathStr: str = "/home/nsynovic/downloads/linux"
    df: DataFrame = DataFrame()

    repo: Repository = Repository(path=pathStr)

    commitWalker: Walker = git.getCommitWalker(repo=repo)

    commit: Commit
    for commit in commitWalker:
        information: CommitInformation = CommitInformation(commit=commit)

        df = pandas.concat([df, information.__pd__()])

    df.to_json("test.json")

    commitPairs: pairwise = createCommitPairing(commits=commitWalker)

    # args: Namespace = mainArgs()

    # directory: PurePath = PurePath(args.directory)
    # directoryChecks: filesystemChecks = testPath(path=directory)


if __name__ == "__main__":
    main()
