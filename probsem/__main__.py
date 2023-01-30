import argparse
import datetime

from probsem.probsem import ProbSem
from probsem.abstract import Object


class CLI(Object):
    def __init__(self) -> None:
        super().__init__()
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument("--prompt", required=True)
        self._parser.add_argument("--test", required=True)
        self._parser.add_argument("--model", default="code-davinci-002")
        self._parser.add_argument("--norm", default=False, action="store_true")
        self._parser.add_argument("--temp", default=1.0, type=float)

    def run_main(self) -> None:
        start = datetime.datetime.now()
        ProbSem(**vars(self._parser.parse_args())).run()
        elapsed = datetime.datetime.now() - start
        self.info(f"Completed successfully in {elapsed}.")


if __name__ == "__main__":
    CLI().run_main()
