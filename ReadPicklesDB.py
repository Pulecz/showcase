import pickle

with open('database.db', 'rb') as iowrap:  # read as bytes
    data = pickle.load(iowrap)

data  # won't get printed when code runs
