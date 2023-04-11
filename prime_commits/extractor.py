import logging
from argparse import Namespace
from warnings import filterwarnings

from prime_commits.args.extractorArgs import getArgs
from prime_commits.extractors import git, hg
from prime_commits.utils.config import Config

filterwarnings(action="ignore")


def main() -> None:
    args: Namespace = getArgs()
    config: Config = Config(args=args)

    logging.basicConfig(
        filename=config.LOG,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )

    match args.vcs:
        case "git":
            git.main(config=config)
        case "hg":
            hg.main(config=config)
        case _:
            exit(1)


if __name__ == "__main__":
    main()
