import logging
import subprocess
from pathlib import Path
from subprocess import CompletedProcess

from pygit2 import GIT_SORT_REVERSE, Repository, Walker

from prime_commits.vcs.genericVCS import GenericVCS


class Git(GenericVCS):
    def __init__(self, repositoryPath: Path) -> None:
        self.repositoryPath: Path = repositoryPath
        self.repo: Repository = Repository(
            path=self.repositoryPath.absolute().__str__()
        )
        super().__init__()

    def checkIfBranch(self, branch: str) -> bool:
        if self.repo.lookup_branch(branch) is None:
            logging.info(msg=f"{branch} is not a valid Git branch")
            return False
        logging.info(msg=f"{branch} is a valid Git branch")
        return True

    def getDefaultBranchName(self) -> str:
        cmdStr: str = "git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'"
        process: CompletedProcess = subprocess.run(
            args=cmdStr, stdout=subprocess.PIPE, shell=True
        )
        branch: str = process.stdout.decode().strip()
        logging.info(msg=f"{branch} is the default Git branch")
        return branch

    def getCommitCount(self, branch: str = "HEAD") -> int:
        cmdStr: str = f"git --no-pager rev-list --count {branch}"
        process: CompletedProcess = subprocess.run(
            args=cmdStr, stdout=subprocess.PIPE, shell=True
        )
        count: int = int(process.stdout)
        logging.info(msg=f"Found {count} commits in branch {branch}")
        return count

    def restoreRepoToBranch(self, branch: str) -> None:
        cmdStr: str = f"git checkout {branch} --quiet --force"
        subprocess.run(args=cmdStr, stdout=subprocess.DEVNULL, shell=True)
        logging.info(msg=f"Restored repo to {branch} branch")

    def getCurrentCheckedOutCommit(self) -> str:
        cmdStr: str = 'git --no-pager log -1 --pretty="%H"'
        process: CompletedProcess = subprocess.run(
            args=cmdStr, stdout=subprocess.PIPE, shell=True
        )
        commit: str = process.stdout.decode().strip()
        logging.info(msg=f"{commit} is currently checked out")
        return commit

    def getCommitIterator(self) -> Walker:
        logging.info(msg=f"Created commit iterator")
        return self.repo.walk(self.repo.head.target, GIT_SORT_REVERSE)


# def checkIfBranch(branch: str, repo: Repository) -> bool:
#     if repo.lookup_branch(branch) is None:
#         logging.info(msg=f"{branch} is not a valid Git branch")
#         return False
#     logging.info(msg=f"{branch} is a valid Git branch")
#     return True


# def getDefaultBranchName() -> str:
#     cmdStr: str = (
#         "git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'"
#     )
#     process: CompletedProcess = subprocess.run(
#         args=cmdStr, stdout=subprocess.PIPE, shell=True
#     )
#     branch: str = process.stdout.decode().strip()
#     logging.info(msg=f"{branch} is the default Git branch")
#     return branch


# def getCommitCount(branch: str = "HEAD") -> int:
#     cmdStr: str = f"git --no-pager rev-list --count {branch}"
#     process: CompletedProcess = subprocess.run(
#         args=cmdStr, stdout=subprocess.PIPE, shell=True
#     )
#     count: int = int(process.stdout)
#     logging.info(msg=f"Found {count} commits in branch {branch}")
#     return count


# def checkoutCommit(commitID: str) -> None:
#     cmdStr: str = f"git checkout {commitID} --quiet --force"
#     subprocess.run(args=cmdStr, stdout=subprocess.DEVNULL, shell=True)
#     logging.info(msg=f"Checked out {commitID}")


# def restoreRepoToBranch(branch: str) -> None:
#     cmdStr: str = f"git checkout {branch} --quiet --force"
#     subprocess.run(args=cmdStr, stdout=subprocess.DEVNULL, shell=True)
#     logging.info(msg=f"Restored repo to {branch} branch")


# def getCurrentCheckedOutCommit() -> str:
#     cmdStr: str = 'git --no-pager log -1 --pretty="%H"'
#     process: CompletedProcess = subprocess.run(
#         args=cmdStr, stdout=subprocess.PIPE, shell=True
#     )
#     commit: str = process.stdout.decode().strip()
#     logging.info(msg=f"{commit} is currently checked out")
#     return commit


# def getCommitIterator(repo: Repository) -> Walker:
#     logging.info(msg=f"Created commit iterator")
#     return repo.walk(repo.head.target, GIT_SORT_REVERSE)
