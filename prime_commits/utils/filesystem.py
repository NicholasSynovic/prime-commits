import logging
from os import chdir, getcwd
from os.path import exists
from pathlib import Path

import hglib
from hglib.error import ServerError
from pygit2 import discover_repository


def checkIfValidDirectoryPath(path: Path) -> bool:
    if exists(path):
        self.LOGGER.info(msg=f"{path} is a valid directory path")
        return True
    self.LOGGER.info(msg=f"{path} is not a valid directory path")
    return False


def checkIfGitRepository(path: Path) -> bool:
    repo: str | None = discover_repository(path.__str__())

    if type(repo) is str:
        self.LOGGER.info(f"{path} is a Git repository")
        return True
    self.LOGGER.info(f"{path} is not a Git repository")
    return False


def checkIfHGRepository(path: Path) -> bool:
    try:
        hglib.open(path=path.__str__()).close()
        self.LOGGER.info(f"{path} is a Mercurial repository")
        return True
    except ServerError:
        self.LOGGER.info(f"{path} is not a Mercurial repository")
        return False


def switchDirectories(path: Path) -> None:
    self.LOGGER.info(msg=f"Now working in {path}")
    chdir(path=path)


def getCWD() -> Path:
    cwd: Path = Path(getcwd()).resolve()
    self.LOGGER.info(msg=f"The current working directory is {cwd}")
    return cwd
