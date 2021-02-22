"""
This module handles parsing by line.

Used for Line of Code Counts and Comment counts
"""


class LineParser:
    def __init__(self, filename: str) -> None:
        self._file = filename
        self.loc: int = 0
        self.comments: int = 0
        self.blank: int = 0
        self.total: int = 0

    def parse(self) -> dict[str, int]:
        self.loc = 0
        self.comments = 0
        self.blank = 0
        self.total = 0

        with open(self._file, "r") as f:
            for line in f.readlines():
                line = line.strip()

                if line == "":
                    self.blank += 1
                elif line.startswith("#"):
                    self.comments += 1
                # Future, add detection of trailing comments.
                # Maybe use rfind to grab the last # if not startswith #
                # then check for any unbalanced '/" trailing it?
                # look at how github.com/psf/black and even the python AST
                # module handle it.
                else:
                    self.loc += 1

                self.total += 1

        return {
            "loc": self.loc,
            "comments": self.comments,
            "blank": self.blank,
            "total": self.total,
        }
