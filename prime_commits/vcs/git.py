from typing import List

from progress.spinner import Spinner
from pygit2 import GIT_SORT_REVERSE, Repository
from pygit2._pygit2 import Commit, Walker


def getCommitList(repo: Repository) -> List[Commit]:
    data: List[Commit] = []

    repoWalker: Walker = repo.walk(repo.head.target, GIT_SORT_REVERSE)

    with Spinner("Getting a list of commits...") as spinner:
        commit: Commit
        for commit in repoWalker:
            data.append(commit)
            spinner.next()

    return data
