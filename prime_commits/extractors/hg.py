import logging
from pathlib import Path

import hglib
from hglib.client import hgclient

from prime_commits.utils import filesystem
from prime_commits.utils.types.config import Config
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
    commitIterator = hg.getCommitIterator(branch=config.BRANCH, repo=repo)

    # if config.BRANCH is None:
    #     config.BRANCH = "default"

    # logging.info(msg=f"Using the {config.BRANCH} branch of {config.PATH}")
