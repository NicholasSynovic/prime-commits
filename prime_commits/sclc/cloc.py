import subprocess
from subprocess import CompletedProcess


def countLines_GIT(commitID: str, branch: str = "HEAD") -> None:
    cmdStr: str = f"cloc --git {commitID} --json"
    process: CompletedProcess = subprocess.run(
        args=cmdStr, stdout=subprocess.PIPE, shell=True
    )
    print(process.stdout)
