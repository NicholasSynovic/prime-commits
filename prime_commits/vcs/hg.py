from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import hglib
from hglib.client import hgclient

from prime_commits.utils.config import Config
from prime_commits.vcs.genericVCS import GenericVCS


class Hg(GenericVCS):
    def __init__(self, repositoryPath: Path, config: Config) -> None:
        self.config = config
        self.repositoryPath: Path = repositoryPath
        self.repo: hgclient = hglib.open(path=self.repositoryPath.absolute().__str__())
        super().__init__()

    def getDefaultBranchName(self) -> str:
        branch: str = self.repo.branch().decode().strip()
        self.config.LOGGER.info(msg=f"{branch} is the default Mercurial branch")
        return branch

    def checkIfBranch(self, branch: str) -> bool:
        detailedBranches: List[Tuple[bytes, int, bytes]] = self.repo.branches(
            closed=True
        )
        branches: List[str] = [branch.decode() for branch, _, _ in detailedBranches]

        try:
            branches.index(branch)
            self.config.LOGGER.info(msg=f"{branch} is a valid Git branch")
            return True
        except ValueError:
            self.config.LOGGER.info(msg=f"{branch} is not a valid Git branch")
            return False

    def restoreRepoToBranch(self, branch: str) -> None:
        self.repo.update(rev=branch, clean=True)
        self.config.LOGGER.info(msg=f"Restored repo to {branch} branch")

    def getCommitIterator(
        self, branch: str
    ) -> List[Tuple[bytes, bytes, bytes, bytes, bytes, bytes]]:
        log = self.repo.log(branch=branch, removed=True)
        self.config.LOGGER.info(msg=f"Created commit iterator for branch {branch}")
        return log

    def getCommitCount(
        self,
        commitIterator: List[Tuple[bytes, bytes, bytes, bytes, bytes, bytes, datetime]],
    ) -> int:
        count: int = len(commitIterator)
        self.config.LOGGER.info(msg=f"Found {count} commits")
        return count

    def checkoutCommit(self, commitID: str) -> None:
        self.repo.update(rev=commitID, clean=True)
        self.config.LOGGER.info(msg=f"Checked out {commitID}")

    def getCurrentCheckedOutCommit(self) -> str:
        return super().getCurrentCheckedOutCommit()
