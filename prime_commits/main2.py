from itertools import pairwise
from typing import List

from pygit2 import Repository
from pygit2._pygit2 import Walker

from prime_commits.vcs import git
from prime_commits.vcs.general import createCommitPairing


def main() -> None:
    pathStr: str = "/home/nsynovic/downloads/linux"
    repo: Repository = Repository(path=pathStr)
    commitWalker: Walker = git.getCommitWalker(repo=repo)
    commitPairs: pairwise = createCommitPairing(commits=commitWalker)

    # args: Namespace = mainArgs()

    # directory: PurePath = PurePath(args.directory)
    # directoryChecks: filesystemChecks = testPath(path=directory)


if __name__ == "__main__":
    main()
