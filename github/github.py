from config    import GITHUB_TOKEN, GITHUB_REPO
from requests  import get, post
from json      import dump
from datetime  import datetime
from math      import ceil


# Debug function
def time_spent(func):
    """
    The function counts the time taken to fetch all issues from the repository
    :param func: function
    :return:     function result
    """
    def wrapper(*args, **kwargs):
        start  = datetime.now()
        result = func(*args, **kwargs)
        print(f'[{func.__name__}]Time spent: {datetime.now() - start}')

        return result

    return wrapper


def fetch_repo_info():
    """
    This function returns general repository data, description, number of issues
    * issues count - issues, pull requests, discussions
    :return: tuple: (Repository description, Issues pages count)
    """
    headers   = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3.raw'
    }
    urls      = [
        fr'https://api.github.com/repos/{GITHUB_REPO}',
        fr'https://api.github.com/repos/{GITHUB_REPO}/issues?state=all'
    ]
    responses = []

    for url in urls:
        responses.append(get(url, headers=headers).json())

    description  = responses[0]['description']
    issues_count = ceil(responses[1][0]['number'] / 100)

    # Convert description to plain text, removes unnecessary characters. Thanks a lot, Inlife! :D
    if description is not None:
        description = sub(r'[^a-zA-Zа-яА-Я0-9\s.,!?-]', '', description).strip()

    return description, issues_count


def fetch_comments(url: str):
    """
    The function sends a request for comments if the response is not an empty .json file and increments the page index
    by 1, otherwise the loop will abort
    :param url:   str: GitHub authorization token
    :return:     list: List of issue comments
    """
    headers    = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3.raw'
    }
    page_index = 1  # Let's start with one, because page 1 is equivalent to page 0
    comments   = []

    while True:
        params   = {'page': page_index, 'per_page': 100}
        request  = get(url, params=params, headers=headers)
        response = request.json()

        if response:
            for comment in response:
                comments.append(comment['body'])

        else:
            break

        page_index += 1

    return comments


@time_spent
def fetch_issue():
    """
    The function will collect information from pages as long as a non-empty .json file comes from the page, increasing
    the page index by 1 each iteration. If .json is empty, the loop will break
    :return:     list: List of issues
    """
    headers    = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3.raw'
    }
    page_index = 1  # Let's start with one, because page 1 is equivalent to page 0
    issues     = []

    while True:
        url      = fr'https://api.github.com/repos/{GITHUB_REPO}/issues'
        params   = {"state": "all", "page": page_index, "per_page": 100}
        request  = get(url, params=params, headers=headers)
        response = request.json()
        print(f'Fetching: {page_index}')

        if response:
            for issue in response:
                issues.append({'Name'   : issue['title'],
                               'Status' : issue['state'],
                               'Author' : issue['user']['login'],
                               'Tags'   : [tag['name'].replace('type:', '') for tag in issue['labels']],
                               'Text'   : issue['body'],
                               'URL'    : issue['url'],
                               'Number' : issue['number'],
                               'C_Count': issue['comments']})
        # 'Comments' : fetch_comments(token, issue['comments_url'])
        else:
            break

        page_index += 1

    return issues
