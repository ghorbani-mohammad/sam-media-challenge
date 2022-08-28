from collections import Counter
from matplotlib import pyplot as plt
from datetime import date, timedelta

from load import Loader
from preprocess import Preprocess


class Analyze:
    def __init__(
        self,
        users,
        transactions,
        merged,
        unsubscribed_users,
        services,
        operators,
        affiliates,
        oses,
        transactions_statuses,
    ):
        self.users = users
        self.transactions = transactions
        self.merged = merged
        self.unsubscribed_users = unsubscribed_users
        self.services = services
        self.operators = operators
        self.affiliates = affiliates
        self.oses = oses
        self.transactions_statuses = transactions_statuses

    def __order_dict__(self, data, reverse=False):
        return {
            k: v
            for k, v in sorted(
                data.items(), key=lambda item: item[1], reverse=reverse
            )
        }

    def __get_os_services_count__(self, data, os):
        result = {}
        for service in self.services:
            result[service] = len(
                data[(data["os_name"] == os) & (data["service"] == service)]
            )
        return result

    def __sum_array__(self, a, b, c=None, d=None):
        result = list(map(lambda x, y: x + y, a, b))
        if c:
            result = list(map(lambda x, y: x + y, result, c))
        if d:
            result = list(map(lambda x, y: x + y, result, d))
        return result

    def __june_days__(self):
        start_date = date(2022, 6, 1)
        end_date = date(2022, 6, 30)
        delta = end_date - start_date
        return range(delta.days + 1)

    def __date_counter__(self, data):
        result = {}
        for item in data:
            item = item.split()[0]
            result[item] = result.get(item, 0) + 1
        return result

    def __complete_days__(self, data):
        keys = []
        start_date = date(2022, 6, 1)
        for i in self.__june_days__():
            day = str(start_date + timedelta(days=i))
            keys.append(day)
            data[day] = data.get(day, 0)
        return keys, data

    def __complete_days_counter__(self, data):
        result = self.__date_counter__(data)
        keys, result = self.__complete_days__(result)
        return keys, result

    def draw_01_distribution_of_services(self):
        services_count = {}
        for service in self.services:
            services_count[service] = len(
                self.users[self.users["service"] == service]
            )
        services_count = self.__order_dict__(services_count)
        keys = list(services_count.keys())
        values = list(services_count.values())
        plt.title("Distribution of Services")
        plt.pie(
            values, labels=keys, explode=[0, 0, 0, 0, 0.1], autopct="%1.1f%%"
        )
        plt.show()

    def draw_02_distribution_of_affiliates(self):
        affiliates_count = {}
        for affiliate in self.affiliates:
            affiliates_count[affiliate] = len(
                self.users[self.users["affiliate"] == affiliate]
            )
        affiliates_count = self.__order_dict__(affiliates_count)
        keys = list(affiliates_count.keys())
        values = list(affiliates_count.values())
        plt.title("Distribution of Affiliates")
        plt.pie(values, labels=keys, explode=[0, 0, 0.1], autopct="%1.1f%%")
        plt.xlabel("Nan values are ignored (near to zero)")
        plt.show()

    def draw_03_distribution_of_oses(self):
        oses_count = {}
        for os in self.oses:
            count = len(self.users[self.users["os_name"] == os])
            if count > 100:  # here we ignore minor oses
                oses_count[os] = count
        oses_count = self.__order_dict__(oses_count)
        keys = list(oses_count.keys())
        values = list(oses_count.values())
        plt.title("Distribution of OSes")
        plt.pie(values, labels=keys, explode=[0, 0.1], autopct="%1.1f%%")
        plt.xlabel(
            "Just considered OS that have at least 50 users. OS X, Windows Phone, iPadOS, HarmonyOS was ignored."
        )
        plt.show()

    def draw_04_most_famous_os_bar(self):
        oses_count = {}
        for os in self.oses:
            oses_count[os] = len(self.users[self.users["os_name"] == os])
        oses_count = self.__order_dict__(oses_count)
        keys = list(oses_count.keys())
        values = list(oses_count.values())
        plt.title("Most Famous OS")
        plt.bar(keys, values)
        for i in range(len(keys)):  # show values on top of bars
            plt.annotate(
                str(values[i]),
                xy=(keys[i], values[i]),
                ha="center",
                va="bottom",
            )
        plt.show()

    def draw_05_service_per_os(self):
        android_services_count = self.__get_os_services_count__(
            data=self.users, os="Android"
        )
        ios_services_count = self.__get_os_services_count__(
            data=self.users, os="iOS"
        )
        android_services_count = self.__order_dict__(
            android_services_count, reverse=True
        )
        ios_services_count = self.__order_dict__(
            ios_services_count, reverse=True
        )

        keys = ["Android", "iOS"]
        values1 = list(android_services_count.values())
        values2 = list(ios_services_count.values())

        y1 = [values1[0], values2[0]]
        y2 = [values1[1], values2[1]]
        y3 = [values1[2], values2[2]]
        y4 = [values1[3], values2[3]]
        y5 = [values1[4], values2[4]]

        plt.bar(keys, y1)
        plt.bar(keys, y2, bottom=y1)
        plt.bar(keys, y3, bottom=self.__sum_array__(y1, y2))
        plt.bar(keys, y4, bottom=self.__sum_array__(y1, y2, y3))
        plt.bar(keys, y5, bottom=self.__sum_array__(y1, y2, y3, y4))
        plt.title("Services/OS")
        plt.legend(self.services)
        plt.ylabel("Users Number")
        plt.show()

    def draw_06_unsubscription_per_service_per_os(self):
        u_users = self.unsubscribed_users
        unsubscribed_android_services_count = self.__get_os_services_count__(
            data=u_users, os="Android"
        )
        unsubscribed_ios_services_count = self.__get_os_services_count__(
            data=u_users, os="iOS"
        )
        unsubscribed_android_services_count = self.__order_dict__(
            unsubscribed_android_services_count, reverse=True
        )
        unsubscribed_ios_services_count = self.__order_dict__(
            unsubscribed_ios_services_count, reverse=True
        )

        keys = ["Android", "iOS"]
        values1 = list(unsubscribed_android_services_count.values())
        values2 = list(unsubscribed_ios_services_count.values())

        y1 = [values1[0], values2[0]]
        y2 = [values1[1], values2[1]]
        y3 = [values1[2], values2[2]]
        y4 = [values1[3], values2[3]]
        y5 = [values1[4], values2[4]]

        plt.bar(keys, y1)
        plt.bar(keys, y2, bottom=y1)
        plt.bar(keys, y3, bottom=self.__sum_array__(y1, y2))
        plt.bar(keys, y4, bottom=self.__sum_array__(y1, y2, y3))
        plt.bar(keys, y5, bottom=self.__sum_array__(y1, y2, y3, y4))
        plt.title("Services/OS")
        plt.legend(self.services)
        plt.ylabel("Unsubscribed Users Count")
        plt.show()

    def draw_07_subscription_per_day(self):
        keys, subscriptions_date_count = self.__complete_days_counter__(
            self.users.subscription_date
        )
        plt.bar([key[5:] for key in keys], subscriptions_date_count.values())
        plt.xticks(rotation=90)
        plt.title("Subscription/Date")
        plt.xlabel("June Month")
        plt.ylabel("Subscription Count")
        plt.show()

    def draw_08_unsubscription_per_day(self):
        keys, unsubscriptions_date_count = self.__complete_days_counter__(
            self.unsubscribed_users.subscription_date
        )
        plt.bar([key[5:] for key in keys], unsubscriptions_date_count.values())
        plt.xticks(rotation=90)
        plt.title("UnSubscription/Date")
        plt.xlabel("June Month")
        plt.ylabel("UnSubscription Count")
        plt.show()

    def draw_09_ps_subscription_per_day(self):
        ps_users = self.users[self.users.service == "ps"]
        keys, subscriptions_date_count = self.__complete_days_counter__(
            ps_users.subscription_date
        )
        plt.bar([key[5:] for key in keys], subscriptions_date_count.values())
        plt.xticks(rotation=90)
        plt.title("PS-Subscription/Date")
        plt.xlabel("June Month")
        plt.ylabel("Subscription Count")
        plt.show()

    def draw_10_ps_unsubscription_per_day(self):
        u_users = self.unsubscribed_users
        ps_unsubscribed_users = u_users[u_users.service == "ps"]
        keys, subscriptions_date_count = self.__complete_days_counter__(
            ps_unsubscribed_users.subscription_date
        )
        plt.bar([key[5:] for key in keys], subscriptions_date_count.values())
        plt.xticks(rotation=90)
        plt.title("PS-UnSubscription/Date")
        plt.xlabel("June Month")
        plt.ylabel("UnSubscription Count")
        plt.show()

    def draw_11_transaction_status(self):
        statuses_count = {}
        for status in self.transactions_statuses:
            statuses_count[status] = len(
                self.transactions[self.transactions["status"] == status]
            )
        statuses_count = self.__order_dict__(statuses_count)
        keys = list(statuses_count.keys())
        values = list(statuses_count.values())
        plt.title("Transactions Statuses")
        plt.pie(values, labels=keys, explode=[0, 0, 0.1], autopct="%1.1f%%")
        plt.xlabel("Nan values are ignored (near to zero)")
        plt.show()

    def draw_12_transaction_status_per_service(self):
        y = []
        for status in self.transactions_statuses:
            temp = []
            for service in self.services:
                temp.append(
                    len(
                        self.transactions[
                            (self.transactions.status == status)
                            & (self.transactions.service == service)
                        ]
                    )
                )
            y.append(temp)
        plt.bar(self.services, y[0])
        plt.bar(self.services, y[1], bottom=y[0])
        plt.bar(
            self.services,
            y[2],
            bottom=list(map(lambda x, y: x + y, y[0], y[1])),
        )
        plt.title("TransactionService/Status")
        plt.legend(self.transactions_statuses)
        plt.xlabel("Service")
        plt.ylabel("Number")
        plt.show()

    def draw_13_transaction_status_per_operator(self):
        y = []
        for status in self.transactions_statuses:
            temp = []
            for operator in self.operators:
                temp.append(
                    len(
                        self.transactions[
                            (self.transactions.status == status)
                            & (self.transactions.phone_operator == operator)
                        ]
                    )
                )
            y.append(temp)
        plt.bar(self.operators, y[0])
        plt.bar(self.operators, y[1], bottom=y[0])
        plt.bar(
            self.operators,
            y[2],
            bottom=list(map(lambda x, y: x + y, y[0], y[1])),
        )
        plt.title("TransactionOperator/Status")
        plt.legend(self.transactions_statuses)
        plt.xlabel("Operator")
        plt.ylabel("Number")
        plt.show()

    def draw_14_transaction_status_per_affiliate(self):
        y = []
        for status in self.transactions_statuses:
            temp = []
            for affiliate in self.affiliates:
                temp.append(
                    len(
                        self.merged[
                            (self.merged.status == status)
                            & (self.merged.affiliate == affiliate)
                        ]
                    )
                )
            y.append(temp)
        plt.bar(self.affiliates, y[0])
        plt.bar(self.affiliates, y[1], bottom=y[0])
        plt.bar(
            self.affiliates,
            y[2],
            bottom=list(map(lambda x, y: x + y, y[0], y[1])),
        )
        plt.title("TransactionAffiliate/Status")
        plt.legend(self.transactions_statuses)
        plt.xlabel("Affiliate")
        plt.ylabel("Number")
        plt.show()

    def draw_15_transaction_status_per_os(self):
        y = []
        for status in self.transactions_statuses:
            temp = []
            for os in self.oses:
                temp.append(
                    len(
                        self.merged[
                            (self.merged.status == status)
                            & (self.merged.os_name == os)
                        ]
                    )
                )
            y.append(temp)
        plt.bar(self.oses, y[0])
        plt.bar(self.oses, y[1], bottom=y[0])
        plt.bar(
            self.oses, y[2], bottom=list(map(lambda x, y: x + y, y[0], y[1]))
        )
        plt.title("TransactionOS/Status")
        plt.legend(self.transactions_statuses)
        plt.xlabel("OS")
        plt.ylabel("Number")
        plt.show()

    def draw_16_transaction_per_user(self):
        same_user_count = {}
        for user_id in self.transactions.user_id:
            same_user_count[user_id] = same_user_count.get(user_id, 0) + 1
        same_user_purchase_counter = Counter(same_user_count.values())
        keys = sorted(same_user_purchase_counter.keys())
        values = []
        keys2 = []
        for item in keys:
            if same_user_purchase_counter[item] > 100:
                keys2.append(item)
                values.append(same_user_purchase_counter[item])
        plt.bar(keys2, values)
        plt.title("Transactions/Users")
        plt.xlabel("Number of Transaction")
        plt.ylabel("Number of Users")
        plt.show()

    def draw_17_delivered_transaction_per_user(self):
        same_user_count = {}
        for user_id in self.transactions[
            self.transactions.status == "Delivered"
        ].user_id:
            same_user_count[user_id] = same_user_count.get(user_id, 0) + 1
        same_user_purchase_counter = Counter(same_user_count.values())
        keys = sorted(same_user_purchase_counter.keys())
        values = []
        keys2 = []
        for item in keys:
            if same_user_purchase_counter[item] > 100:
                keys2.append(item)
                values.append(same_user_purchase_counter[item])
        plt.bar(keys2, values)
        plt.title("DeliveredTransactions/Users")
        plt.xlabel("Number of Delivered Transaction")
        plt.ylabel("Number of Users")
        plt.show()


class Draw:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def draw(self):
        draw_methods = [
            method_name
            for method_name in dir(self.analyzer)
            if callable(getattr(self.analyzer, method_name))
            and "__" not in method_name
        ]
        draw_all = False
        for method in draw_methods:
            if not draw_all:
                resp = input(f"{method}? (y/n/all) ")
            if resp == "all":
                draw_all = True
            if resp == "y" or draw_all:
                func = getattr(self.analyzer, method)
                func()


loader = Loader("data\\users.csv", "data\\transactions.tsv")

preprocessed_data = Preprocess(loader.users_data, loader.transactions_data)
preprocessed_data.extract_entities()

analyzer = Analyze(
    users=loader.users_data,
    transactions=loader.transactions_data,
    merged=loader.merged_data,
    unsubscribed_users=preprocessed_data.unsubscribed_users,
    services=preprocessed_data.services,
    operators=preprocessed_data.operators,
    affiliates=preprocessed_data.affiliates,
    oses=preprocessed_data.oses,
    transactions_statuses=preprocessed_data.transactions_statuses,
)

drawer = Draw(analyzer)
drawer.draw()
