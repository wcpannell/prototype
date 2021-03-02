from typing import Dict, List, Optional
from sys import argv, exit, stderr
from copy import deepcopy
from os.path import isfile

from parsing.CSVBuilder import CSVBuilder
from parsing.parsing import Parsing, add_dicts, EMPTY_METRICS


class CLI:
    """A Entity class containing configuration data passed in from the user"""

    filenames: Optional[List[str]] = None
    outfile: Optional[str] = None
    _Parser: Parsing
    _Writer: CSVBuilder
    _metrics: Dict[str, int] = deepcopy(EMPTY_METRICS)

    def __init__(self):
        self.configure(argv[1:])  # Ignore first argument (this filename)

    def configure(self, args: List[str]) -> None:
        isoutfile: bool = False

        # Process Arguments
        for argument in args:
            if argument == "--output":
                isoutfile = True
            elif isoutfile:
                self.outfile = argument
            else:
                if isfile(argument):
                    if self.filenames is not None:
                        self.filenames.append(argument)
                    else:
                        self.filenames = [argument]
                else:
                    print(
                        f"File named '{argument}' not found.\n exiting...",
                        file=stderr,
                    )
                    exit(1)

    def run(self) -> None:
        if self.outfile is None:
            self.outfile = "output.csv"

        if self.filenames is None:
            print(
                "No files selected. Pass source files as arguments.",
                file=stderr,
            )
            print(
                "Pass --output filename.csv as a pair of arguments to set the output filename",
                file=stderr,
            )
            exit(2)
        else:
            for filename in self.filenames:
                print(f"Processing {filename}...")
                self._Parser = Parsing(filename=filename)
                add_dicts(self._Parser.parse(), self._metrics)

            self._Writer = CSVBuilder(self.outfile, self._metrics)
            self._Writer.build()


if __name__ == "__main__":
    app = CLI()
    app.run()
    print(f"Processing Complete.")
