import pandas as pd


class Loader:
    def __init__(self, path: str, sep=None) -> None:
        self.data = pd.read_csv(path, sep=sep)
