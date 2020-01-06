import GetYoutubeLinks


def get_new_links():
    data = GetYoutubeLinks.get_submissions_from_subreddit('documentaries')
    return data


if __name__ == '__main__':
    data = get_new_links()
