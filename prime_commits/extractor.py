from argparse import Namespace

from prime_commits.args.extractorArgs import getArgs
from prime_commits.extractors import git, hg


def main() -> None:
    args: Namespace = getArgs()

    match args.vcs:
        case "git":
            git.main(args=args)
        case "hg":
            hg.main(args=args)
        case _:
            exit(1)


if __name__ == "__main__":
    main()
