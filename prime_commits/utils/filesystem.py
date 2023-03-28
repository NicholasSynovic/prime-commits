from collections import namedtuple
from os.path import exists
from pathlib import PurePath
from typing import Type

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
    gitPath: PurePath = PurePath(path, ".git")
    return exists(path=gitPath)
