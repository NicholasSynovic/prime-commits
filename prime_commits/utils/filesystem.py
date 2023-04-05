import logging
from os import chdir, getcwd
from os.path import exists
from pathlib import Path

from pygit2 import discover_repository


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
    logging.info(msg=f"Now working in {path}")
    chdir(path=path)


def getCWD() -> Path:
    cwd: Path = Path(getcwd()).resolve()
    logging.info(msg=f"The current working directory is {cwd}")
    return cwd
