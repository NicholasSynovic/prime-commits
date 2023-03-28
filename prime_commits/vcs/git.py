from typing import List

from pygit2 import GIT_SORT_REVERSE, Repository
from pygit2._pygit2 import Commit


def getCommitList(repo: Repository) -> List[Commit]:
    data: List[Commit] = []

    commit: Commit
    for commit in repo.walk(repo.head.target, GIT_SORT_REVERSE):
        data.append(commit)

    return data
