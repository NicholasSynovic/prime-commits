from collections import namedtuple
from os import chdir
from os.path import exists
from pathlib import PurePath

from pygit2 import discover_repository

filesystemChecks = namedtuple(
    typename="RepoChecks", field_names=["IS_DIR", "IS_GIT"], defaults=[False, False]
)


def testPath(path: PurePath) -> filesystemChecks:
    return filesystemChecks(
        IS_DIR=checkIfValidDirectoryPath(path), IS_GIT=checkIfGitRepository(path)
    )


def checkIfValidDirectoryPath(path: PurePath) -> bool:
    return exists(path)


def checkIfGitRepository(path: PurePath) -> bool:
    return discover_repository(path.__str__())


def switchDirectories(path: PurePath) -> None:
    chdir(path=path)
