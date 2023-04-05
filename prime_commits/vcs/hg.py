import logging
from datetime import datetime
from typing import List, Tuple

from hglib.client import hgclient


def getDefaultBranchName(repo: hgclient) -> str:
    branch: str = repo.branch()
    logging.info(msg=f"{branch} is the default Mercurial branch")
    return branch


def checkIfBranch(branch: str, repo: hgclient) -> bool:
    detailedBranches: List[Tuple[bytes, int, bytes]] = repo.branches(closed=True)
    branches: List[str] = [branch.decode() for branch, _, _ in detailedBranches]

    try:
        branches.index(branch)
        logging.info(msg=f"{branch} is a valid Git branch")
        return True
    except ValueError:
        logging.info(msg=f"{branch} is not a valid Git branch")
        return False


def restoreRepoToBranch(branch: str, repo: hgclient) -> None:
    repo.update(rev=branch, clean=True)
    logging.info(msg=f"Restored repo to {branch} branch")


def getCommitIterator(
    branch: str, repo: hgclient
) -> List[Tuple[bytes, bytes, bytes, bytes, bytes, bytes]]:
    log = repo.log(branch=branch, removed=True)
    logging.info(msg=f"Created commit iterator for branch {branch}")
    return log


def getCommitCount(
    commitIterator: List[Tuple[bytes, bytes, bytes, bytes, bytes, bytes, datetime]]
) -> int:
    count: int = len(commitIterator)
    logging.info(msg=f"Found {count} commits")
    return count
