class Preprocess:
    def __init__(self, users, transactions) -> None:
        self.users = users
        self.transactions = transactions

    def get_services(self):
        return list(set(self.users.service))

    def get_operators(self):
        return list(set(self.users.phone_operator))

    def get_affiliates(self):
        return list(set(self.users[self.users["affiliate"].notna()].affiliate))

    def get_oses(self):
        return list(set(self.users[self.users["os_name"].notna()].os_name))

    def get_transaction_statuses(self):
        return list(
            set(self.transactions[self.transactions["status"].notna()].status)
        )

    def extract_entities(self) -> None:
        self.services = self.get_services()
        self.operators = self.get_operators()
        self.affiliates = self.get_affiliates()
        self.oses = self.get_oses()
        self.transactions_statuses = self.get_transaction_statuses()
