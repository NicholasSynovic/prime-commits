from argparse import ArgumentParser, Namespace
from importlib.metadata import version
from pathlib import PurePath

import prime_commits.args as argVars


def getArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=argVars.programName,
        usage="To extract commit and source code line counts (SCLC) from each commit of a branch of a Git repository",
        epilog=f"Authors: {','.join(argVars.authorNames)}",
    )
    parser.add_argument(
        "-d", "--directory", type=PurePath, required=True, help="A Git directory"
    )
    parser.add_argument(
        "-b",
        "--branch",
        default=None,
        type=str,
        required=False,
        help="A  branch name of the Git repository to be analyzed",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=PurePath("commits.json"),
        type=PurePath,
        required=False,
        help="Output file to store commit and SCLC data in JSON format",
    )
    parser.add_argument(
        "-l",
        "--log",
        default=PurePath("commits.log"),
        type=PurePath,
        required=False,
        help="File to store logging information",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{argVars.programName}: {version(distribution_name='prime-commits')}",
    )
    return parser.parse_args()
