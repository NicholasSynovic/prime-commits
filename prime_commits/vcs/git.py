from pygit2 import GIT_SORT_REVERSE, Repository
from pygit2._pygit2 import Walker


def getCommitWalker(repo: Repository) -> Walker:
    return repo.walk(repo.head.target, GIT_SORT_REVERSE)
