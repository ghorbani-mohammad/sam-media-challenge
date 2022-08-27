import pandas as pd
from matplotlib import pyplot as plt

from load import Loader


users = Loader(path="data\\users.csv", sep=",").file
transactions = Loader(path="data\\transactions.tsv", sep="\t").file


total_user_rows = len(users) - 1
services = set(users.service)

# count each services
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

affiliates = set(users.affiliate)
affiliates_count = {}
for affiliate in affiliates:
    affiliates_count[affiliate] = len(users[users["affiliate"] == affiliate])
affiliates_count = {
    k: v for k, v in sorted(affiliates_count.items(), key=lambda item: item[1])
}

keys = list(affiliates_count.keys())[1:]
values = list(affiliates_count.values())[1:]

plt.title("Most Famous Affiliate")
plt.pie(values, labels=keys, explode=[0, 0, 0.1], autopct="%1.1f%%")
plt.xlabel("Nan values are ignored (near to zero)")
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

for i in range(delta.days + 1):
    day = str(start_date + timedelta(days=i))
    subscriptions_date_count[day] = subscriptions_date_count.get(day, 0)

plt.bar(
    [key[5:] for key in subscriptions_date_count.keys()],
    subscriptions_date_count.values(),
)
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

for i in range(delta.days + 1):
    day = str(start_date + timedelta(days=i))
    unsubscriptions_date_count[day] = unsubscriptions_date_count.get(day, 0)

plt.bar(
    [key[5:] for key in unsubscriptions_date_count.keys()],
    unsubscriptions_date_count.values(),
)
plt.xticks(rotation=90)
plt.title("UnSubscription/Date")
plt.xlabel("Date")
plt.ylabel("UnSubscription Count")
plt.show()
