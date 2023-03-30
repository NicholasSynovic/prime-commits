import subprocess
from subprocess import CompletedProcess

from pygit2 import GIT_SORT_REVERSE, Branch, Repository, Walker


def checkIfBranch(branch: str, repo: Repository) -> bool:
    print(repo.branches)


def getCommitWalker(repo: Repository) -> Walker:
    return repo.walk(repo.head.target, GIT_SORT_REVERSE)


def getCommitCount_CMDLINE(branch: str = "HEAD") -> int:
    cmdStr: str = f"git --no-pager rev-list --count {branch}"

    process: CompletedProcess = subprocess.run(
        args=cmdStr, stdout=subprocess.PIPE, shell=True
    )
    return int(process.stdout)


def checkoutCommit_CMDLINE(commitID: str) -> None:
    cmdStr: str = f"git checkout {commitID} --quiet --force"
    subprocess.run(args=cmdStr, stdout=subprocess.DEVNULL, shell=True)


def getCurrentCheckedOutCommit_CMDLINE() -> str:
    cmdStr: str = 'git --no-pager log -1 --pretty="%H"'
    process: CompletedProcess = subprocess.run(
        args=cmdStr, stdout=subprocess.PIPE, shell=True
    )
    return process.stdout.decode().strip()


def resetHEAD_CMDLINE(branch: str) -> None:
    cmdStr: str = f"git switch {branch} --quiet --force"
    subprocess.run(args=cmdStr, stdout=subprocess.DEVNULL, shell=True)
