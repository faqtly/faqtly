from requests  import get
from json      import dump
from datetime  import datetime


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


def headers(token: str):
    """
    :param token: str: GitHub authorization token
    :return:     dict: Request headers
    """
    return {
        'Authorization': f'token {token}',
        'Accept'       : 'application/vnd.github.v3.raw'
    }


def fetch_readme(token: str, repo: str):
    """
    :param token: str: GitHub authorization token
    :param repo:  str: Repository Owner/Name of GitHub Repository
    :return:      str: README repository file if it exists, otherwise None
    """
    url    = fr"https://api.github.com/repos/{repo}/contents/README.md"
    readme = get(url, headers=headers(token)).text
    error  = '{"message":"Not Found",' \
             '"documentation_url":"https://docs.github.com/rest/repos/contents#get-repository-content"}'

    return readme if readme != error else None


def fetch_comments(token: str, url: str):
    """
    The function sends a request for comments if the response is not an empty .json file and increments the page index
    by 1, otherwise the loop will abort
    :param token: str: GitHub authorization token
    :param url:   str: GitHub authorization token
    :return:     list: List of issue comments
    """
    page_index = 1  # Let's start with one, because page 1 is equivalent to page 0
    comments   = []

    while True:
        params   = {'page': page_index, 'per_page': 100}
        requests = get(url, params=params, headers=headers(token))
        response = requests.json()

        if response:
            for comment in response:
                comments.append(comment['body'])

        else:
            break

        page_index += 1

    return comments


@time_spent
def fetch_issue(token: str, repo: str):
    """
    The function will collect information from pages as long as a non-empty .json file comes from the page, increasing
    the page index by 1 each iteration. If .json is empty, the loop will break
    :param token: str: GitHub authorization token
    :param repo:  str: Owner/Name of GitHub Repository
    :return:     list: List of issues
    """
    page_index = 1  # Let's start with one, because page 1 is equivalent to page 0
    issues     = []

    while True:
        url      = fr'https://api.github.com/repos/{repo}/issues'
        params   = {"state": "all", "page": page_index, "per_page": 100}
        request  = get(url, params=params, headers=headers(token))
        response = request.json()
        print(f'Fetching: {page_index}')

        if response:
            for issue in response:
                issues.append({'Name'  : issue['title'],
                               'Status': issue['state'],
                               'Author': issue['user']['login'],
                               'Tags'  : [tag['name'].replace('type:', '') for tag in issue['labels']],
                               'Text'  : issue['body'],
                               'URL'   : issue['url'],
                               'Number': issue['number'],
                               'Comments' : fetch_comments(token, issue['comments_url'])})  # comments url
        else:
            break

        page_index += 1

    return issues
