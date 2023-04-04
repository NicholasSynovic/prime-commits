import numpy
from typedframe import TypedDataFrame


class SCLCInformation(TypedDataFrame):
    schema: dict = {
        "Files": numpy.int16,
        "Lines": numpy.int16,
        "Blank": numpy.int16,
        "Comment": numpy.int16,
        "Code": numpy.int16,
    }
