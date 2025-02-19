from argparse import ArgumentParser, Namespace

REPO: str = "https://raw.githubusercontent.com/dpinela/DeathsDoor.Randomizer"
COMMIT: str = "main"
LOGIC_LOCATION: str = "Randomizer/Logic"
OUTPUT: str = "../logic.json"

class Args:
    repo: str
    commit: str
    path: str
    output: str

    def __init__(self):
        parser = ArgumentParser(
            "extract.py",
            description="Automatic extraction of components from DD Rando core"
        );

        parser.add_argument(
            "-r", "--repo",
            default=REPO,
            help=f"URL of the repo containing the logic files. (default={REPO})"
        )
        parser.add_argument(
            "-c", "--commit",
            default=COMMIT,
            help=f"The commit id from which to base the extraction. (default={COMMIT})"
        )
        parser.add_argument(
            "-p", "--path",
            default=LOGIC_LOCATION,
            help=f"Path where the logic files are contained within the repository. (default={LOGIC_LOCATION})"
        )
        parser.add_argument(
            "-o", "--output",
            default=OUTPUT,
            help=f"Output location of the extracted logic. (default={OUTPUT})"
        )

        parser.parse_args(namespace=self)

    def url(self) -> str:
        return f"{self.repo}/{self.commit}/{self.path}"

    def __str__(self) -> str:
        return f"Args {{ repo: {self.repo}; commit: {self.commit}; path: {self.path} }}"
