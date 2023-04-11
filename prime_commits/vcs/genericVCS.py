from abc import ABCMeta, abstractmethod
from typing import Any


# https://realpython.com/python-interface/#formal-interfaces
class GenericVCS(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "checkIfBranch")
            and callable(subclass.checkIfBranch)
            and hasattr(subclass, "getDefaultBranchName")
            and callable(subclass.getDefaultBranchName)
            and hasattr(subclass, "getCommitCount")
            and callable(subclass.getCommitCount)
            and hasattr(subclass, "checkoutCommit")
            and callable(subclass.checkoutCommit)
            and hasattr(subclass, "restoreRepoToBranch")
            and callable(subclass.restoreRepoToBranch)
            and hasattr(subclass, "getCurrentCheckedOutCommit")
            and callable(subclass.getCurrentCheckedOutCommit)
            and hasattr(subclass, "getCommitIterator")
            and callable(subclass.getCommitIterator)
            or NotImplemented
        )

    @abstractmethod
    def checkIfBranch(branch: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def getDefaultBranchName() -> str:
        raise NotImplementedError

    @abstractmethod
    def getCommitCount(branch: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def checkoutCommit(commitID: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def restoreRepoToBranch(branch: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def getCurrentCheckedOutCommit() -> str:
        raise NotImplementedError

    @abstractmethod
    def getCommitIterator() -> Any:
        raise NotImplementedError
