import CONSTS

import pickle
with open(CONSTS.db_name, 'rb') as iowrap:  # read as bytes
    data = pickle.load(iowrap)

data  # won't get printed when code runs
