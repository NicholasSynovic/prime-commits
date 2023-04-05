import logging
from pathlib import Path

import hglib
from hglib.client import hgclient

from prime_commits.utils.types.config import Config


def main(config: Config) -> None:
    repo: hgclient = hglib.open(path=config.PATH)

    # if config.BRANCH is None:
    #     config.BRANCH = "default"

    # logging.info(msg=f"Using the {config.BRANCH} branch of {config.PATH}")
