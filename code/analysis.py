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


oses = set(users.os_name)
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
