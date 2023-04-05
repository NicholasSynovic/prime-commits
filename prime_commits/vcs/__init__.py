from abc import ABCMeta


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
