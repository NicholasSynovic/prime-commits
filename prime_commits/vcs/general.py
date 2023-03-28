from itertools import pairwise
from typing import Any, List


def createCommitPairing(commits: List[Any]) -> pairwise:
    return pairwise(commits)
