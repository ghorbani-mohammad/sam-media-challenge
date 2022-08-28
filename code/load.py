import pandas as pd


class Loader:
    def __init__(self, users_path, transaction_path) -> None:
        self.users_data = pd.read_csv(users_path, sep=",")
        self.transactions_data = pd.read_csv(transaction_path, sep="\t")
        self.merged_data = pd.merge(
            self.users_data, self.transactions_data, how="inner", on="user_id"
        )
