from collections import namedtuple
from os import chdir, getcwd
from os.path import exists
from pathlib import Path

from pygit2 import discover_repository

filesystemChecks = namedtuple(
    typename="RepoChecks", field_names=["IS_DIR", "IS_GIT"], defaults=[False, False]
)


def testPath(path: Path) -> filesystemChecks:
    return filesystemChecks(
        IS_DIR=checkIfValidDirectoryPath(path), IS_GIT=checkIfGitRepository(path)
    )


def checkIfValidDirectoryPath(path: Path) -> bool:
    return exists(path)


def checkIfGitRepository(path: Path) -> bool:
    return discover_repository(path.__str__())


def switchDirectories(path: Path) -> None:
    chdir(path=path)


def getCWD() -> Path:
    return Path(getcwd())
