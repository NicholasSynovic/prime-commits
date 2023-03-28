from argparse import Namespace
from pathlib import PurePath

from args import mainArgs

from prime_commits.utils.filesystem import filesystemChecks, testPath


def main() -> None:
    args: Namespace = mainArgs()

    directory: PurePath = PurePath(args.directory)
    directoryChecks: filesystemChecks = testPath(path=directory)


if __name__ == "__main__":
    pass
