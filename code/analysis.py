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
