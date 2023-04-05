import logging
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
    if exists(path):
        logging.info(msg=f"{path} is a valid directory path")
        return True
    logging.info(msg=f"{path} is not a valid directory path")
    return False


def checkIfGitRepository(path: Path) -> bool:
    isRepo: str | None = discover_repository(path.__str__())

    if type(isRepo) is str:
        logging.info(f"{path} is a Git repository")
        return True
    logging.info(f"{path} is not a Git repository")
    return False


def switchDirectories(path: Path) -> None:
    chdir(path=path)


def getCWD() -> Path:
    return Path(getcwd()).resolve()
