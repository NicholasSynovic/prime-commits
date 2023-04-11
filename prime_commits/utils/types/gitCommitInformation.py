from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pandas import DataFrame
from pygit2 import Signature
from pygit2._pygit2 import Commit

from prime_commits.utils.types.jsonSchema import schema


class GitCommitInformation:
    def __init__(self, commit: Commit) -> None:
        author: Signature = commit.author
        commiter: Signature = commit.committer

        self.id: str = commit.id.__str__()
        self.CommitDate: int = commit.commit_time  # Unix timestamp
        self.CommitMessage: str = commit.message.strip()
        self.AuthorName: str = author.name
        self.AuthorEmail: str = author.email
        self.AuthorDate: int = author.time  # Unix timestamp
        self.CommiterName: str = commiter.name
        self.CommiterEmail: str = commiter.email
        self.CommiterDate: int = commiter.time  # Unix timestamp

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
