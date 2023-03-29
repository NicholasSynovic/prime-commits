from typing import List

from pandas import DataFrame
from pygit2 import Signature
from pygit2._pygit2 import Commit


class CommitInformation:
    def __init__(self, commit: Commit) -> None:
        author: Signature = commit.author
        committer: Signature = commit.committer

        self.id: str = commit.id.__str__()
        self.CommitTime: int = commit.commit_time  # Unix timestamp
        self.CommitMessage: str = commit.message.strip()
        self.AuthorName: str = author.name
        self.AuthorEmail: str = author.email
        self.AuthorDate: int = author.time  # Unix timestamp
        self.CommitterName: str = committer.name
        self.CommitterEmail: str = committer.email
        self.CommitterDate: int = committer.time  # Unix timestamp

        self.NumberOfFiles: int = 0
        self.NumberOfLines: int = 0
        self.NumberOfBlankLines: int = 0
        self.NumberOfCommentLines: int = 0
        self.LOC: int = 0
        self.KLOC: int = 0
        self.SCC_Complexity: int = 0
        self.Bytes: int = 0

    def __pd__(self) -> DataFrame:
        return DataFrame.from_dict(data=self.__dict__, orient="index").T
