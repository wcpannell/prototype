"""
This module handles parsing by line.

Used for Line of Code Counts and Comment counts
"""

from typing import Dict, List
from copy import deepcopy
import ast

EMPTY_METRICS: Dict[str, int] = {
    "NOL": 0,
    "NOC": 0,
    "CPES": 0,
    "NOCL": 0,
    "NNC1": 0,
    "NNC2": 0,
    "NNC3": 0,
    "NNC4": 0,
    "NNC5": 0,
    "NNC6": 0,
    "NNC7": 0,
    "NNC8": 0,
    "NNC9": 0,
    "NNC10": 0,
    "NNC": 0,
    "NOM": 0,
    "NIM": 0,
    "NLM": 0,
    "NOVM": 0,
    "ANIM": 0,
    "ANLM": 0,
    "NOH": 0,
    "NAC": 0,
    "NLC": 0,
    "NPPM": 0,
    "NOA": 0,
    "AWI": 0,
}


class LineParser:
    """Line based statistics"""

    def __init__(self, filename: str) -> None:
        self._file: str = filename
        self.loc: int = 0
        self.comments: int = 0
        self.blank: int = 0
        self.total: int = 0

    def parse(self) -> Dict[str, int]:
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
            "NOL": self.loc,
            "NOC": self.comments,
            "blank": self.blank,
            "total": self.total,
        }


class AstParser:
    """Metrics measurements based on abstract syntax tree data"""

    def __init__(self, filename: str) -> None:
        self.tree: ast.AST
        with open(filename, "r") as source:
            self.tree = ast.parse(source.read())

    def parse(self) -> Dict[str, int]:
        """Parses AST Tree

        This is currently implemented as a recursive function. It will blow up
        on a large enough file. This should change before a production release.
        """
        return _recursive_parse(self.tree, depth=0)


def add_dicts(fromdict: Dict[str, int], todict: Dict[str, int]):
    for key, value in fromdict.items():
        if key in todict.keys():
            todict[key] += value
        else:
            todict[key] = value


def _recursive_parse(ast_obj: ast.AST, depth: int = 0) -> Dict[str, int]:
    output = deepcopy(EMPTY_METRICS)

    try:
        body: List = ast_obj.body
    except AttributeError:
        body = list()

    for obj in body:
        if isinstance(obj, ast.ClassDef):
            output["NOCL"] += 1

            # This counts classes nested by composition
            if depth > 1:
                if depth < 10:
                    output[f"NNC{depth}"] += 1
                else:
                    # Count classes 10 and deeper as level 10
                    output["NNC10"] += 1
                output["NNC"] += 1

            # Identify parents.
            # This is needed for properly identifying local methods vs
            # inherited which cannot be accomplished in this prototype
            for parent in obj.bases:
                if parent.id != "object":
                    # for now, just prove that we can find the parent
                    print(f"{obj.name} is a child of {parent.id}")

        if isinstance(obj, ast.FunctionDef):
            output["NOM"] += 1

        # Count docstrings as comments
        if isinstance(obj, ast.Expr):
            if isinstance(obj.value, ast.Constant) and isinstance(
                obj.value.value, str
            ):
                output["NOC"] += obj.value.end_lineno - obj.value.lineno + 1

        lower = _recursive_parse(obj, depth + 1)
        add_dicts(lower, output)

    return output


class Parsing:
    _LineParsing: LineParser
    _AstParsing: AstParser

    def __init__(self, filename: str) -> None:
        self._LineParsing = LineParser(filename=filename)
        self._AstParsing = AstParser(filename=filename)

    def parse(self) -> Dict[str, int]:
        self._metrics = self._AstParsing.parse()
        add_dicts(self._LineParsing.parse(), self._metrics)
        return self._metrics


if __name__ == "__main__":
    from sys import argv, exit

    if len(argv) == 2:
        filename = argv[1]
    else:
        print("just call this with a filename for testing")
        exit()

    lp = LineParser(filename)
    ap = AstParser(filename)
    print(lp.parse())
    print(ap.parse())
