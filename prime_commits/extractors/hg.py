import logging
from typing import List, Tuple

import hglib
from hglib.client import hgclient
from progress.bar import Bar

from prime_commits.utils import filesystem
from prime_commits.utils.types.config import Config
from prime_commits.utils.types.gitCommitInformation import CommitInformation
from prime_commits.vcs import hg


def main(config: Config) -> None:
    if filesystem.checkIfHGRepository(path=config.PATH) == False:
        exit(1)
    repo: hgclient = hglib.open(path=config.PATH.__str__())

    if config.BRANCH is None:
        config.BRANCH: str = hg.getDefaultBranchName(repo=repo)

    if hg.checkIfBranch(branch=config.BRANCH, repo=repo) == False:
        exit(2)
    else:
        logging.info(msg=f"Using the {config.BRANCH} branch of {config.PATH}")

    hg.restoreRepoToBranch(branch=config.BRANCH, repo=repo)
    commitIterator: List[
        Tuple[bytes, bytes, bytes, bytes, bytes, bytes]
    ] = hg.getCommitIterator(branch=config.BRANCH, repo=repo)
    commitCount: int = hg.getCommitCount(commitIterator=commitIterator)

    with Bar("Extracting commit information...", max=commitCount) as bar:
        commit: Tuple[bytes, bytes, bytes, bytes, bytes, bytes]
        for commit in commitIterator:
            information: CommitInformation = CommitInformation()
