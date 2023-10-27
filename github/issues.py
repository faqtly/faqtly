from github.github     import github_request
from time              import time
from math              import ceil
from asyncio           import create_task, gather
from aiohttp           import ClientSession


# Debug function
def time_spent(func):
    """
    The function counts the time taken to fetch all issues from the repository
    :param func: func
    :return:     func()
    """
    async def wrapper(*args, **kwargs):
        start  = time()
        result = await func(*args, **kwargs)
        print(f'[{func.__name__}]Time spent: {(time() - start):.1f}')

        return result

    return wrapper


async def fetch_pages_count():
    """
    The function sends a request to the last issue page and gets the id of the last issue,
    then the total number of pages with issues is determined by the formula
    :return: int: Number of pages
    """
    async with ClientSession() as session:
        response = await github_request(session, '/issues?state=all')

    return ceil(response[0]['number'] / 100)


async def gather_comments(url: str, count: int):
    """
    The function creates n-tasks to send requests for comments (pages)
    :param url:   str: Comments URL
    :param count: int: Pages count
    :return:     list: List of comments
    """
    tasks    = []
    comments = []

    async with ClientSession() as session:
        for page_index in range(1, count + 1):
            params = {"page": page_index, "per_page": 100}
            tasks.append(create_task(github_request(session, url, params=params)))

        # TODO: This needs to be replaced, otherwise the data will not be received correctly,
        # TODO: but I haven't figured out what the error is yet
        r_comments = [i for comments in await gather(*tasks) for i in comments if isinstance(comments, list)]

        for comment in r_comments:
            comments.append(comment['body'])

    return comments


@time_spent
async def gather_issues():
    """
    The function creates n-tasks to send requests for issues
    Then creates n-tasks to send requests for comments (issues)
    :return: list: List of issues
    """
    tasks   = []
    issues  = []
    total_p = await fetch_pages_count()

    async with ClientSession() as session:
        # Creating tasks (issues)
        for page_index in range(1, total_p + 1):
            params = {"state": "all", "page": page_index, "per_page": 100}
            tasks.append(create_task(github_request(session, '/issues', params=params)))

        # Data acquisition and processing (issues)
        for issue in [i for issues in await gather(*tasks) for i in issues]:
            issues.append({'Name'   : issue['title'],
                           'Text'   : issue['body'],
                           'URL'    : issue['url'],
                           'Number' : issue['number'],
                           'C_Pages': ceil(issue['comments'] / 100),
                           'I_URL'  : issue['comments_url']})
        else:
            tasks.clear()

        # Creating tasks (comments)
        for issue in issues:
            tasks.append(create_task(gather_comments(issue['I_URL'], issue['C_Pages'])))

        # Data acquisition and processing (comments)
        comments = await gather(*tasks)
        for number, issue in enumerate(issues):
            issue['Comments'] = comments[number]

    return issues
