import csv
import json
from argparse import ArgumentParser

import pandas
from pandas import DataFrame
from pandas.io.json import json_normalize


def get_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="Convert Output",
        usage="This program converts a JSON file into various different formats.",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="The input JSON file that is to be converted",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--csv",
        help="Flag to set the output of the conversion to a .csv file",
        default=None,
        type=bool,
        required=False,
    )
    parser.add_argument(
        "--tsv",
        help="Flag to set the output of the conversion to a .tsv file",
        default=None,
        type=bool,
        required=False,
    )
    return parser


def createDataframe(filename: str) -> DataFrame:
    return pandas.read_json(filename)


def convertToCSV(df: DataFrame, filename: str) -> None:
    df.to_csv(filename, index=False)


def convertToTSV(df: DataFrame, filename: str) -> None:
    df.to_csv(filename, sep="\t", index=False)


if __name__ == "__main__":
    args = get_argparse()
    df: DataFrame = createDataframe("output.json")
    convertToCSV(df, "output.csv")
    convertToTSV(df, "output.tsv")
