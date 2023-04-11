from os import chdir, getcwd
from os.path import exists
from pathlib import Path

import hglib
from hglib.error import ServerError
from pygit2 import discover_repository

from prime_commits.utils.config import Config


def checkIfValidDirectoryPath(path: Path, config: Config) -> bool:
    if exists(path):
        config.LOGGER.info(msg=f"{path} is a valid directory path")
        return True
    config.LOGGER.info(msg=f"{path} is not a valid directory path")
    return False


def checkIfGitRepository(path: Path, config: Config) -> bool:
    repo: str | None = discover_repository(path.__str__())

    if type(repo) is str:
        config.LOGGER.info(f"{path} is a Git repository")
        return True
    config.LOGGER.info(f"{path} is not a Git repository")
    return False


def checkIfHGRepository(path: Path, config: Config) -> bool:
    try:
        hglib.open(path=path.__str__()).close()
        config.LOGGER.info(f"{path} is a Mercurial repository")
        return True
    except ServerError:
        config.LOGGER.info(f"{path} is not a Mercurial repository")
        return False


def switchDirectories(path: Path, config: Config) -> None:
    config.LOGGER.info(msg=f"Now working in {path}")
    chdir(path=path)


def getCWD(config: Config) -> Path:
    cwd: Path = Path(getcwd()).resolve()
    config.LOGGER.info(msg=f"The current working directory is {cwd}")
    return cwd
