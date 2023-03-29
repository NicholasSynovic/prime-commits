import subprocess
from subprocess import CompletedProcess

from pygit2 import GIT_SORT_REVERSE, Repository
from pygit2._pygit2 import Walker


def getCommitWalker(repo: Repository) -> Walker:
    return repo.walk(repo.head.target, GIT_SORT_REVERSE)


def getCommitCount_CMDLINE(repo: Repository, branch: str = "HEAD") -> int:
    cmdStr: str = f"git --no-pager -C {repo.path} rev-list --count {branch}"

    process: CompletedProcess = subprocess.run(
        args=cmdStr, stdout=subprocess.PIPE, shell=True
    )
    return int(process.stdout)
