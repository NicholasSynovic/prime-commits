def graphArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Git Commit LOC Exploder Grapher",
        description=f"A tool for graphing LOC information from the output of the {name} Commit LOC Exploder",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "-i",
        "--input",
        help=f"JSON export from {name} Git Commit Exploder. DEFAULT: ./commits_loc.json",
        type=str,
        required=False,
        default="commits_loc.json",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Filename of the graph. DEFAULT: ./commits_loc.pdf",
        type=str,
        required=False,
        default="commits_loc.pdf",
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
        help="Display version of the tool",
        action="store_true",
        default=False,
    )
    return parser.parse_args()
