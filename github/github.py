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
        start = datetime.now()
        result = func(*args, **kwargs)
        print(f'[Fetch Issues]Time spent: {datetime.now() - start}')

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
    readme = get(f"https://api.github.com/repos/{repo}/contents/README.md", headers=headers(token)).text
    error  = '{"message":"Not Found",' \
             '"documentation_url":"https://docs.github.com/rest/repos/contents#get-repository-content"}'

    return readme if readme != error else None


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
        url     = fr'https://api.github.com/repos/{repo}/issues?state=all&page={page_index}'
        request = get(url, headers=headers(token))

        if request.json():
            for issue in request.json():
                issues.append({'Name'  : issue['title'],
                               'Status': issue['state'],
                               'Author': issue['user']['login'],
                               'Tags'  : [tag['name'].replace('type:', '') for tag in issue['labels']],
                               'Text'  : issue['body'],
                               'URL'   : issue['url'],
                               'Number': issue['number']})
        else:
            break

        page_index += 1

    return issues
