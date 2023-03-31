from argparse import ArgumentParser, Namespace
from importlib.metadata import version
from pathlib import Path

import prime_commits.args as argVars

programName: str = f"{argVars.programName} Graph Utility"


def getArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=programName,
        description=f"To graph commit and source code line counts (SCLC) from each commit of a branch of a Git repository",
        epilog=f"Author(s): {', '.join(argVars.authorNames)}",
    )

    parser.add_argument(
        "-i",
        "--input",
        help=f"JSON export from {argVars.programName} Git Commit Exploder",
        type=Path,
        required=False,
        default=Path("commits.json").resolve(),
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Filename of the graph",
        type=Path,
        required=False,
        default=Path("commits.pdf").resolve(),
    )
    parser.add_argument(
        "-x",
        help="Key of the X values to use for graphing",
        type=str,
        required=False,
        default="CommitDaysSince0",
    )
    parser.add_argument(
        "-y",
        help="Key of the Y values to use for graphing",
        type=str,
        required=False,
        default="KLOC",
    )
    parser.add_argument(
        "--type",
        help="Type of figure to plot",
        choices=["line", "bar"],
        type=str,
        required=False,
        default="line",
    )
    parser.add_argument(
        "--title",
        help="Title of the figure",
        type=str,
        required=False,
        default="KLOC per Day",
    )
    parser.add_argument(
        "--x-label",
        help="X axis label of the figure",
        type=str,
        required=False,
        default="Commit Day Since 0",
    )
    parser.add_argument(
        "--y-label",
        help="Y axis label of the figure",
        type=str,
        required=False,
        default="KLOC",
    )
    parser.add_argument(
        "--stylesheet",
        help="Filepath of a MatPlotLib stylesheet to use",
        type=Path.resolve(),
        required=False,
        default=None,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{programName} {version(distribution_name='prime-commits')}",
    )
    return parser.parse_args()
