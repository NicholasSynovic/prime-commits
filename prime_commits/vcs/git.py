import logging
import subprocess
from subprocess import CompletedProcess

from pygit2 import GIT_SORT_REVERSE, Branch, Repository, Walker


def checkIfBranch(branch: str, repo: Repository) -> bool:
    if repo.lookup_branch(branch) is None:
        logging.info(msg=f"{branch} is not a valid Git branch")
        return False
    logging.info(msg=f"{branch} is a valid Git branch")
    return True


def getDefaultBranchName() -> str:
    cmdStr: str = (
        "git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'"
    )
    process: CompletedProcess = subprocess.run(
        args=cmdStr, stdout=subprocess.PIPE, shell=True
    )
    branch: str = process.stdout.decode().strip()
    logging.info(msg=f"{branch} is a valid Git branch")
    return branch


def getCommitCount(branch: str = "HEAD") -> int:
    cmdStr: str = f"git --no-pager rev-list --count {branch}"
    process: CompletedProcess = subprocess.run(
        args=cmdStr, stdout=subprocess.PIPE, shell=True
    )
    count: int = int(process.stdout)
    logging.info(msg=f"Found {count} commits in branch {branch}")
    return count


def checkoutCommit(commitID: str) -> None:
    cmdStr: str = f"git checkout {commitID} --quiet --force"
    subprocess.run(args=cmdStr, stdout=subprocess.DEVNULL, shell=True)
    logging.info(msg=f"Checked out {commitID}")


def restoreRepoToBranch(branch: str) -> None:
    cmdStr: str = f"git checkout {branch} --quiet --force"
    subprocess.run(args=cmdStr, stdout=subprocess.DEVNULL, shell=True)
    logging.info(msg=f"Restored repo to {branch} branch")


def getCurrentCheckedOutCommit() -> str:
    cmdStr: str = 'git --no-pager log -1 --pretty="%H"'
    process: CompletedProcess = subprocess.run(
        args=cmdStr, stdout=subprocess.PIPE, shell=True
    )
    return process.stdout.decode().strip()


def getCommitWalker(repo: Repository) -> Walker:
    return repo.walk(repo.head.target, GIT_SORT_REVERSE)
