from collections import namedtuple
from types import List

from pygit2 import Signature
from pygit2._pygit2 import Commit

collumns: List[str] = [
    "id",
    "CommitTime",
    "CommitMessage",
    "AuthorName",
    "AuthorEmail",
    "AuthorDate",
    "CommitterName",
    "CommitterEmail",
    "CommitterDate",
]

commitInformation = namedtuple(typename="CommitInformation", field_names=collumns)


def extractCommitInformation(commit: Commit) -> commitInformation:
    id: str = commit.id.__str__()
    author: Signature = commit.author
    committer: Signature = commit.committer

    commitTime: int = commit.commit_time  # Unix timestamp
    commitMessage: str = commit.message
    authorName: str = author.name
    authorEmail: str = author.email
    authorDate: int = author.time  # Unix timestamp
    committerName: str = committer.name
    committerEmail: str = committer.email
    committerDate: str = committer.time

    return commitInformation(
        id=id,
        CommitTime=commitTime,
        CommitMessage=commitMessage,
        AuthorName=authorName,
        AuthorEmail=authorEmail,
        AuthorDate=authorDate,
        CommitterName=committerName,
        CommitterEmail=committerEmail,
        CommitterDate=committerDate,
    )
