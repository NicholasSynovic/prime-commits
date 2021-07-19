from argparse import ArgumentParser, Namespace
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import pandas
from pandas import DataFrame


def get_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="Convert Output",
        usage="This program converts a JSON file into various different formats.",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="The input data file that will be read to create the graphs",
        type=str,
        required=True,
    )
    return parser


def createDataFrame(filename: str, filetype: str = "json") -> DataFrame:
    if filetype == "json":
        return pandas.read_json(filename)
    elif filetype == "csv":
        return pandas.read_csv(filename)
    elif filetype == "tsv":
        return pandas.read_csv(filename, sep="\t")
    else:
        return False


def plot(df: DataFrame) -> None:
    figure: Figure = plt.figure()
    df.plot(kind="bar", x="day", y="loc_sum")
    figure.savefig("test.png")


def helloworld():
    fig = plt.figure()
    plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
    fig.savefig("test.png")


if __name__ == "__main__":
    args: Namespace = get_argparse().parse_args()

    df = createDataFrame(filename="output.json")

    print(df)

    plot(df)
