from argparse import ArgumentParser, Namespace, _SubParsersAction
from importlib.metadata import version
from pathlib import Path

import prime_commits.args as argVars


def getArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=argVars.programName,
        usage="To extract commit and source code line counts (SCLC) from each commit of a branch of a Git repository",
        epilog=f"Authors: {', '.join(argVars.authorNames)}",
        formatter_class=argVars.AlphabeticalOrderHelpFormatter,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{argVars.programName}: {version(distribution_name='prime-commits')}",
    )

    parser.add_argument(
        "--sclc",
        default="scc",
        type=str,
        choices=["scc", "cloc"],
        required=False,
        help="Set the source code line counter to use",
    )

    subparsers: _SubParsersAction = parser.add_subparsers(
        title="Supported VCS",
        required=True,
    )

    gitParser = subparsers.add_parser(
        name="git",
        help="Options for analyzing Git repositories",
        prog=argVars.programName,
        usage="prime-commits git",
    )

    gitParser.add_argument(
        "-d",
        "--directory",
        type=Path,
        required=True,
        help="A Git directory",
        dest="gitDirectory",
    )
    gitParser.add_argument(
        "-b",
        "--branch",
        default=None,
        type=str,
        required=False,
        help="A  branch name of the Git repository to be analyzed",
        dest="gitBranch",
    )
    gitParser.add_argument(
        "-o",
        "--output",
        default=Path("commits.json").resolve(),
        type=Path,
        required=False,
        help="Output file to store commit and SCLC data in JSON format",
        dest="gitOutput",
    )
    gitParser.add_argument(
        "-l",
        "--log",
        default=Path("commits.log").resolve(),
        type=Path,
        required=False,
        help="File to store logging information",
        dest="gitLog",
    )

    return parser.parse_args()
