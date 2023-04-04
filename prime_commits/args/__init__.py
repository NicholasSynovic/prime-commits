from argparse import ArgumentDefaultsHelpFormatter
from typing import List

programName: str = "PRIME Commits Extractor"
authorNames: List[str] = [
    "Nicholas M. Synovic",
    "Matthew Hyatt",
    "George K. Thiruvathukal",
]


class AlphabeticalOrderHelpFormatter(ArgumentDefaultsHelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=lambda x: x.dest)
        super(AlphabeticalOrderHelpFormatter, self).add_arguments(actions)
