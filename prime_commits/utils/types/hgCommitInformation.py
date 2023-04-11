from datetime import datetime
from time import mktime
from typing import List, Tuple

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pandas import DataFrame

from prime_commits.utils.types.jsonSchema import schema


class HgCommitInformation:
    def __init__(
        self, commit: Tuple[bytes, bytes, bytes, bytes, bytes, bytes, datetime]
    ) -> None:
        nameEmail: List[str] = commit[4].decode().strip().split(" ")

        email: str = nameEmail[-1].replace("<", "").replace(">", "")
        name: str = " ".join(nameEmail[0:-1])
        date: int = int(mktime(commit[6].timetuple()))

        self.id: str = commit[1].decode().strip()
        self.CommitDate: int = date  # Unix timestamp
        self.CommitMessage: str = commit[5].decode().strip()
        self.AuthorName: str = name
        self.AuthorEmail: str = email
        self.AuthorDate: int = date  # Unix timestamp
        self.CommiterName: str = name
        self.CommiterEmail: str = email
        self.CommiterDate: int = date  # Unix timestamp

        self.CommitDaysSince0: int = 0
        self.CommiterDaysSince0: int = 0
        self.AuthorDaysSince0: int = 0

        self.NumberOfFiles: int = 0
        self.NumberOfLines: int = 0
        self.NumberOfBlankLines: int = 0
        self.NumberOfCommentLines: int = 0
        self.LOC: int = 0
        self.KLOC: float = 0

        self.DLOC: int = 0
        self.DKLOC: float = 0

    def __pd__(self) -> DataFrame:
        return DataFrame.from_dict(data=self.__dict__, orient="index").T

    def __validate__(self) -> bool:
        try:
            validate(instance=self.__dict__, schema=schema)
            return True
        except ValidationError:
            return False
