from argparse import Namespace
from pathlib import PurePath

from pygit2 import Repository

from prime_commits.args import mainArgs
from prime_commits.utils.filesystem import filesystemChecks, testPath
from prime_commits.vcs import git


def main() -> None:
    pathStr: str = "/home/nsynovic/downloads/linux"

    print("Creating Repository Obj.")
    repo: Repository = Repository(path=pathStr)

    print("Getting Commit List...")
    git.getCommitList(repo)

    # args: Namespace = mainArgs()

    # directory: PurePath = PurePath(args.directory)
    # directoryChecks: filesystemChecks = testPath(path=directory)


if __name__ == "__main__":
    main()
