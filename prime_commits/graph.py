from argparse import Namespace
from pathlib import Path

import matplotlib.pyplot as plt
import pandas
from pandas import DataFrame

from prime_commits.args.graphArgs import getArgs


def computeXY(
    df: DataFrame,
    xKey: str,
    yKey: str,
) -> tuple:
    xData: set = df[xKey].unique().tolist()
    yData: list = []
    day: int

    for day in xData:
        yData.append(df.loc[df[xKey] == day, yKey].sum())
    return (xData, yData)


def plot(
    x: list,
    y: list,
    type: str,
    title: str,
    xLabel: str,
    yLabel: str,
    output: str,
    stylesheet: str,
) -> None:
    if stylesheet != None:
        plt.style.use(Path(stylesheet).resolve())

    match type:
        case "line":
            plt.plot(x, y)
        case "bar":
            plt.bar(x, height=y)
        case _:
            return 1

    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

    plt.savefig(output)


def main() -> None:
    args: Namespace = getArgs()

    df: DataFrame = pandas.read_json(args.input).T

    data: tuple = computeXY(df=df, xKey=args.x, yKey=args.y)
    plot(
        x=data[0],
        y=data[1],
        type=args.type,
        title=args.title,
        xLabel=args.x_label,
        yLabel=args.y_label,
        output=args.output,
        stylesheet=args.stylesheet,
    )


if __name__ == "__main__":
    main()
