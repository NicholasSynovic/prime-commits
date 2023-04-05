from argparse import Namespace

from prime_commits.args.extractorArgs import getArgs
from prime_commits.extractors import git, hg
from prime_commits.utils.types.config import Config


def main() -> None:
    args: Namespace = getArgs()
    config: Config = Config(args=args)

    match args.vcs:
        case "git":
            git.main(config=config)
        case "hg":
            hg.main(config=config)
        case _:
            exit(1)


if __name__ == "__main__":
    main()
