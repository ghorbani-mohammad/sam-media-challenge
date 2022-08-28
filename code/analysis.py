import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt
from datetime import date, timedelta

from load import Loader


users = Loader(path="data\\users.csv", sep=",").data
transactions = Loader(path="data\\transactions.tsv", sep="\t").data
merged_table = pd.merge(users, transactions, how="inner", on="user_id")

services = list(set(users.service))
operators = list(set(users.phone_operator))
affiliates = ["aff_4", "aff_2", "aff_3"]
oses = ["Android", "iOS", "Windows Phone", "iPadOS", "OS X", "HarmonyOS"]
transactions_statuses = ["Failed", "Delivered", "Pending"]

services_count = {}
for service in services:
    services_count[service] = len(users[users["service"] == service])
services_count = {
    k: v for k, v in sorted(services_count.items(), key=lambda item: item[1])
}
keys = list(services_count.keys())
values = list(services_count.values())

plt.title("Most Famous Service")
plt.pie(values, labels=keys, explode=[0, 0, 0, 0, 0.1], autopct="%1.1f%%")
plt.show()


affiliates_count = {}
for affiliate in affiliates:
    affiliates_count[affiliate] = len(users[users["affiliate"] == affiliate])
affiliates_count = {
    k: v for k, v in sorted(affiliates_count.items(), key=lambda item: item[1])
}

keys = list(affiliates_count.keys())
values = list(affiliates_count.values())

plt.title("Most Famous Affiliate")
plt.pie(values, labels=keys, explode=[0, 0, 0.1], autopct="%1.1f%%")
plt.xlabel("Nan values are ignored (near to zero)")
plt.show()


oses_count = {}
for os in oses:
    count = len(users[users["os_name"] == os])
    if count > 100:
        oses_count[os] = count
oses_count = {
    k: v for k, v in sorted(oses_count.items(), key=lambda item: item[1])
}

keys = list(oses_count.keys())
values = list(oses_count.values())

plt.title("Most Famous OS")
plt.pie(values, labels=keys, explode=[0, 0.1], autopct="%1.1f%%")
plt.xlabel(
    "Just considered OS that have at least 50 users. OS X, Windows Phone, iPadOS, HarmonyOS was ignored."
)
plt.show()


oses_count = {}
for os in oses:
    count = len(users[users["os_name"] == os])
    if count > 0:
        oses_count[os] = count
oses_count = {
    k: v for k, v in sorted(oses_count.items(), key=lambda item: item[1])
}

keys = list(oses_count.keys())
values = list(oses_count.values())

plt.title("Most Famous OS")
plt.bar(keys, values)
for i in range(len(keys)):
    plt.annotate(
        str(values[i]), xy=(keys[i], values[i]), ha="center", va="bottom"
    )
plt.show()


android_services_count = {}
for service in services:
    android_services_count[service] = len(
        users[(users["os_name"] == "Android") & (users["service"] == service)]
    )

ios_services_count = {}
for service in services:
    ios_services_count[service] = len(
        users[(users["os_name"] == "iOS") & (users["service"] == service)]
    )


android_services_count = {
    k: v
    for k, v in sorted(
        android_services_count.items(), key=lambda item: item[1], reverse=True
    )
}

ios_services_count = {
    k: v
    for k, v in sorted(
        ios_services_count.items(), key=lambda item: item[1], reverse=True
    )
}

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
plt.bar(keys, y3, bottom=list(map(lambda x, y: x + y, y1, y2)))
plt.bar(
    keys,
    y4,
    bottom=list(map(lambda x, y, z: x + y + z, y1, y2, y3)),
)
plt.bar(
    keys,
    y5,
    bottom=list(map(lambda x, y, z, i: x + y + z + i, y1, y2, y3, y4)),
)
plt.title("Services/OS")
plt.legend(services)
plt.ylabel("Users Number")
plt.show()


unsubscribed_users = users[users["unsubscription_date"].notna()]
unsubscribed_android_services_count = {}
for service in services:
    unsubscribed_android_services_count[service] = len(
        unsubscribed_users[
            (unsubscribed_users["os_name"] == "Android")
            & (unsubscribed_users["service"] == service)
        ]
    )

unsubscribed_ios_services_count = {}
for service in services:
    unsubscribed_ios_services_count[service] = len(
        unsubscribed_users[
            (unsubscribed_users["os_name"] == "iOS")
            & (unsubscribed_users["service"] == service)
        ]
    )

unsubscribed_android_services_count = {
    k: v
    for k, v in sorted(
        unsubscribed_android_services_count.items(),
        key=lambda item: item[1],
        reverse=True,
    )
}

unsubscribed_ios_services_count = {
    k: v
    for k, v in sorted(
        unsubscribed_ios_services_count.items(),
        key=lambda item: item[1],
        reverse=True,
    )
}

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
plt.bar(keys, y3, bottom=list(map(lambda x, y: x + y, y1, y2)))
plt.bar(
    keys,
    y4,
    bottom=list(map(lambda x, y, z: x + y + z, y1, y2, y3)),
)
plt.bar(
    keys,
    y5,
    bottom=list(map(lambda x, y, z, i: x + y + z + i, y1, y2, y3, y4)),
)
plt.title("Services/OS")
plt.legend(services)
plt.ylabel("Unsubscribed Users Count")
plt.show()


subscriptions_date_count = {}
for item in users.subscription_date:
    item = item.split()[0]
    subscriptions_date_count[item] = subscriptions_date_count.get(item, 0) + 1

start_date = date(2022, 6, 1)
end_date = date(2022, 6, 30)
delta = end_date - start_date

keys = []
for i in range(delta.days + 1):
    day = str(start_date + timedelta(days=i))
    keys.append(day)
    subscriptions_date_count[day] = subscriptions_date_count.get(day, 0)

plt.bar([key[5:] for key in keys], subscriptions_date_count.values())
plt.xticks(rotation=90)
plt.title("Subscription/Date")
plt.xlabel("Date")
plt.ylabel("Subscription Count")
plt.show()


unsubscriptions_date_count = {}
for item in unsubscribed_users.subscription_date:
    item = item.split()[0]
    unsubscriptions_date_count[item] = (
        unsubscriptions_date_count.get(item, 0) + 1
    )

start_date = date(2022, 6, 1)
end_date = date(2022, 6, 30)
delta = end_date - start_date

keys = []
for i in range(delta.days + 1):
    day = str(start_date + timedelta(days=i))
    keys.append(day)
    unsubscriptions_date_count[day] = unsubscriptions_date_count.get(day, 0)

plt.bar([key[5:] for key in keys], unsubscriptions_date_count.values())
plt.xticks(rotation=90)
plt.title("UnSubscription/Date")
plt.xlabel("Date")
plt.ylabel("UnSubscription Count")
plt.show()

ps_users = users[users.service == "ps"]
subscriptions_date_count = {}
for item in ps_users.subscription_date:
    item = item.split()[0]
    subscriptions_date_count[item] = subscriptions_date_count.get(item, 0) + 1

start_date = date(2022, 6, 1)
end_date = date(2022, 6, 30)
delta = end_date - start_date

keys = []
for i in range(delta.days + 1):
    day = str(start_date + timedelta(days=i))
    keys.append(day)
    subscriptions_date_count[day] = subscriptions_date_count.get(day, 0)

plt.bar([key[5:] for key in keys], subscriptions_date_count.values())
plt.xticks(rotation=90)
plt.title("PS-Subscription/Date")
plt.xlabel("Date")
plt.ylabel("Subscription Count")
plt.show()


ps_unsubscribed_users = unsubscribed_users[unsubscribed_users.service == "ps"]
subscriptions_date_count = {}
for item in ps_unsubscribed_users.subscription_date:
    item = item.split()[0]
    subscriptions_date_count[item] = subscriptions_date_count.get(item, 0) + 1

start_date = date(2022, 6, 1)
end_date = date(2022, 6, 30)
delta = end_date - start_date

keys = []
for i in range(delta.days + 1):
    day = str(start_date + timedelta(days=i))
    keys.append(day)
    subscriptions_date_count[day] = subscriptions_date_count.get(day, 0)

plt.bar([key[5:] for key in keys], subscriptions_date_count.values())
plt.xticks(rotation=90)
plt.title("PS-UnSubscription/Date")
plt.xlabel("Date")
plt.ylabel("UnSubscription Count")
plt.show()


statuses_count = {}
for status in transactions_statuses:
    statuses_count[status] = len(
        transactions[transactions["status"] == status]
    )
statuses_count = {
    k: v for k, v in sorted(statuses_count.items(), key=lambda item: item[1])
}
keys = list(statuses_count.keys())
values = list(statuses_count.values())

plt.title("Transactions Statuses")
plt.pie(values, labels=keys, explode=[0, 0, 0.1], autopct="%1.1f%%")
plt.xlabel("Nan values are ignored (near to zero)")
plt.show()

y = []
for status in transactions_statuses:
    temp = []
    for service in services:
        temp.append(
            len(
                transactions[
                    (transactions.status == status)
                    & (transactions.service == service)
                ]
            )
        )
    y.append(temp)

plt.bar(services, y[0])
plt.bar(services, y[1], bottom=y[0])
plt.bar(services, y[2], bottom=list(map(lambda x, y: x + y, y[0], y[1])))
plt.title("TransactionService/Status")
plt.legend(transactions_statuses)
plt.xlabel("Service")
plt.ylabel("Number")
plt.show()


y = []
for status in transactions_statuses:
    temp = []
    for operator in operators:
        temp.append(
            len(
                transactions[
                    (transactions.status == status)
                    & (transactions.phone_operator == operator)
                ]
            )
        )
    y.append(temp)

plt.bar(operators, y[0])
plt.bar(operators, y[1], bottom=y[0])
plt.bar(operators, y[2], bottom=list(map(lambda x, y: x + y, y[0], y[1])))
plt.title("TransactionOperator/Status")
plt.legend(transactions_statuses)
plt.xlabel("Operator")
plt.ylabel("Number")
plt.show()


y = []
for status in transactions_statuses:
    temp = []
    for affiliate in affiliates:
        temp.append(
            len(
                merged_table[
                    (merged_table.status == status)
                    & (merged_table.affiliate == affiliate)
                ]
            )
        )
    y.append(temp)
plt.bar(affiliates, y[0])
plt.bar(affiliates, y[1], bottom=y[0])
plt.bar(affiliates, y[2], bottom=list(map(lambda x, y: x + y, y[0], y[1])))
plt.title("TransactionAffiliate/Status")
plt.legend(transactions_statuses)
plt.xlabel("Affiliate")
plt.ylabel("Number")
plt.show()


y = []
for status in transactions_statuses:
    temp = []
    for os in oses:
        temp.append(
            len(
                merged_table[
                    (merged_table.status == status)
                    & (merged_table.os_name == os)
                ]
            )
        )
    y.append(temp)
plt.bar(oses, y[0])
plt.bar(oses, y[1], bottom=y[0])
plt.bar(oses, y[2], bottom=list(map(lambda x, y: x + y, y[0], y[1])))
plt.title("TransactionOS/Status")
plt.legend(transactions_statuses)
plt.xlabel("OS")
plt.ylabel("Number")
plt.show()


same_user_count = {}
for user_id in transactions.user_id:
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


same_user_count = {}
for user_id in transactions[transactions.status == "Delivered"].user_id:
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
