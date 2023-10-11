from config            import GITHUB_REPO, GITHUB_TOKEN
from github.repository import issue_pages
from requests          import get
from time              import time
from math              import ceil
from asyncio           import create_task, gather, run
from aiohttp           import ClientSession


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


async def fetch_comments(session: object, url: str, params: dict):
    """
    The function sends an async request to a page with comments
    :param session: object: Async session
    :param url:        str: Comment URL
    :param params:    dict: Request parameters
    :return:          list: List of comments from the current page
    """
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3.raw'
    }
    print('Comments')
    async with session.get(url=url, params=params, headers=headers) as response:
        response = await response.json()
        comments = []

        for comment in response:
            comments.append(comment['body'])

        return comments


async def gather_comments(url: str, count: int):
    """
    The function creates n-number of tasks to send requests
    :param url:   str: Comments URL
    :param count: int: Pages count
    :return:     list: List of comments
    """
    async with ClientSession() as session:
        tasks = []

        for page_index in range(1, count + 1):
            params = {"state": "all", "page": page_index, "per_page": 100}
            tasks.append(create_task(fetch_comments(session, url, params)))

        return [i for comments in await gather(*tasks) for i in comments]


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
    print('Issue')
    async with session.get(url=url, params=params, headers=headers) as response:
        response = await response.json()
        issues   = []
        for issue in response:
            comments_pages = ceil(issue['comments'] / 100)

            issues.append({'Name'    : issue['title'],
                           'Status'  : issue['state'],
                           'Author'  : issue['user']['login'],
                           'Tags'    : [tag['name'].replace('type:', '') for tag in issue['labels']],
                           'Text'    : issue['body'],
                           'URL'     : issue['url'],
                           'Number'  : issue['number'],
                           'Comments': await gather_comments(issue['comments_url'], comments_pages)})

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
