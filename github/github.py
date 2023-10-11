from config   import GITHUB_TOKEN, GITHUB_REPO
from requests import get, post
from json     import dump
from time     import time
from math     import ceil
from re       import sub
from aiohttp  import ClientSession
from asyncio  import create_task, gather


# Debug function
def time_spent(func):
    """
    The function counts the time taken to fetch all issues from the repository
    :param func: function
    :return:     function result
    """
    async def wrapper(*args, **kwargs):
        start  = time()
        result = await func(*args, **kwargs)
        print(f'[{func.__name__}]Time spent: {round(time() - start, 2)}')

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


repo_description, issue_pages = fetch_repo_info()


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


async def fetch_issue(session: object, url: str, params: dict):
    """
    The function sends an async request to a page with an issues
    :param session: object: Async session
    :param url:        str: Issues url
    :param params:     str: Request parameters
    :return:          list: List of issues from the current page
    """
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3.raw'
    }

    async with session.get(url=url, params=params, headers=headers) as response:
        response = await response.json()
        issues   = []
        for issue in response:
            issues.append({'Name'   : issue['title'],
                           'Status' : issue['state'],
                           'Author' : issue['user']['login'],
                           'Tags'   : [tag['name'].replace('type:', '') for tag in issue['labels']],
                           'Text'   : issue['body'],
                           'URL'    : issue['url'],
                           'Number' : issue['number'],
                           'C_Count': issue['comments']})

        return issues


@time_spent
async def gather_issues():
    """
    The function creates n-number of tasks to send requests
    :return: list: List of issues
    """
    async with ClientSession() as session:
        tasks   = []
        url     = fr'https://api.github.com/repos/{GITHUB_REPO}/issues'

        for page_index in range(1, issue_pages + 1):
            params = {"state": "all", "page": page_index, "per_page": 100}
            tasks.append(create_task(fetch_issue(session, url, params)))

        return [i for issues in await gather(*tasks) for i in issues]