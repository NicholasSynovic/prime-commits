from argparse import ArgumentParser, Namespace
from importlib.metadata import version
from pathlib import Path

import prime_commits.args as argVars

programName: str = f"{argVars.programName} Graph Utility"


def getArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=programName,
        usage=f"To graph the data generated from {argVars.programName}",
        epilog=f"Author(s): {', '.join(argVars.authorNames)}",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help=f"JSON data file from {argVars.programName}",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=Path("commits.pdf").resolve(),
        type=Path,
        required=False,
        help="Output file to store the graph of commit information",
    )
    parser.add_argument(
        "-x",
        help="Key of the x values to use for graphing. DEFAULT: author_days_since_0",
        type=str,
        required=False,
        default="author_days_since_0",
    )
    parser.add_argument(
        "-y",
        help="Key of the y values to use for graphing. DEFAULT: lines_of_code",
        type=str,
        required=False,
        default="lines_of_code",
    )
    parser.add_argument(
        "--type",
        help="Type of figure to plot. DEFAULT: line",
        type=str,
        required=False,
        default="line",
    )
    parser.add_argument(
        "--title",
        help='Title of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--x-label",
        help='X axis label of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--y-label",
        help='Y axis label of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--stylesheet",
        help='Filepath of matplotlib stylesheet to use. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{argVars.programName}: {version(distribution_name='prime-commits')}",
    )
    return parser.parse_args()
