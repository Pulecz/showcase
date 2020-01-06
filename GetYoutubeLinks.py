#!/usr/bin/python
import praw  # for reddit API
import pickle  # for data serializing
from os.path import exists as does_file_exist  # for checking if file exist
try:
    import our_secrets
except ImportError:
    print('ha! you are missing the secretsssssss')
    exit(1)  # exit with errrcode 1

# Define data structure
# dict for multiple submissions
    # the reddit's submission ID will be the primary key
dict_of_data = {}
db_name = 'gamedeals.db'

# make an instance from Reddit class defined in praw module
# username and password is for write access, rest is for read only
reddit = praw.Reddit(client_id=our_secrets.client_id,
                     client_secret=our_secrets.client_secret,
                     user_agent=our_secrets.user_agent,
                     username=our_secrets.username,
                     password=our_secrets.password)

# TODO when no internet connectivity (or train wifi with long timeouts)
# skip getting the data and quit gracefully


# work with A subreddit
for submission in reddit.subreddit('videos').hot(limit=50):
    # print("Title: {0}\nscore: {1}\n".format(
        # submission.title, submission.ups))
    # dictionary for details
    data = {'title': submission.title,
            'targetURL': submission.url,
            'redditURL': submission.shortlink,
            "score": submission.ups}
    # save it to the dictionary with submission's reddit id
    dict_of_data[submission.id] = data

# print submissions with highest score first
"""make a list of submussion.ids, highest first (reversed)
x is the submussion.ids iterated in dict_of_data to use ['score'] key
taken from:
https://stackoverflow.com/questions/4110665/
sort-nested-dictionary-by-value-and-remainder-by-another-value-in-python"""
score_list = sorted(dict_of_data,
                    key=lambda x: (dict_of_data[x]['score']), reverse=False)

# score_list should have same length as dict_of_data, let's use .get() anyway
for submission in score_list:
    payload = dict_of_data.get(submission)
    # if no payload, no data (this should never happen)
    # even if this is done on the whole db, not just new data
    if payload:
        print("""Title: {0}
                 score: {1}
                 Turl: {2}
                 Rurl: {3}""".format(
            payload['title'], payload['score'],
            payload['targetURL'], payload['redditURL']))

# in first run, database.db does not exist
# skip reading and appending continue at write the db
if does_file_exist(db_name):
    # file exists, read the db, and load the data
    with open(db_name, 'rb') as iowrap:  # write as bytes
        # load the data from iowrap instance
        old_dict_of_data = pickle.load(iowrap)
    print('INFO: Loaded \'databse.db\'')
    # update the old data with new data and overwrite the old values
    old_dict_of_data.update(dict_of_data)
    # and save it to the dict_of_data
    dict_of_data = old_dict_of_data
# write the db
with open(db_name, 'wb') as iowrap:  # write as bytes
    pickle.dump(dict_of_data, iowrap)  # save the data to iowrap instance
    print('INFO: Saved {0} items \'databse.db\''.format(len(dict_of_data)))
