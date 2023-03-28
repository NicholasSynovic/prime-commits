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
        self.CommitMessage: str = commit.message
        self.AuthorName: str = author.name
        self.AuthorEmail: str = author.email
        self.AuthorDate: int = author.time  # Unix timestamp
        self.CommitterName: str = committer.name
        self.CommitterEmail: str = committer.email
        self.CommitterDate: int = committer.time  # Unix timestamp

    def __pd__(self) -> DataFrame:
        return DataFrame.from_dict(data=self.__dict__, orient="index").T
