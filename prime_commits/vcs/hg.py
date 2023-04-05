import logging
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


def getHEADName() -> None:
    pass
