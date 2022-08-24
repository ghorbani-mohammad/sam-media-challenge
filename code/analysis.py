from load import Loader

users = Loader(path='data\\users.csv', sep=',')
transactions = Loader(path='data\\transactions.tsv', sep='\t')
