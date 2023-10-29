from config        import GITHUB_REPO
from github.github import github_request
from time          import time
from math          import ceil
from asyncio       import create_task, gather


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


async def fetch_pages_count(session: object):
    """
    The function sends a request to the last issue page and gets the id of the last issue,
    then the total number of pages with issues is determined by the formula
    :param session: object: GitHub Session
    :return:           int: Number of pages
    """
    response = await github_request(session, '/issues?state=all')

    return ceil(response[0]['number'] / 100)


async def gather_comments(session: object, url: str, count: int, issue: int):
    """
    The function creates n-tasks to send requests for comments (pages)
    :param session: object: GitHub Session
    :param url:        str: Comments URL
    :param count:      int: Pages count
    :return:          list: List of comments
    """
    tasks    = []
    comments = []

    for page_index in range(1, count + 1):
        params = {"page": page_index, "per_page": 100}
        tasks.append(create_task(github_request(session, url, params=params)))

    # TODO: I think we need to revisit and rewrite this. But it's working properly!
    # PS: You don't need to fix something that works! [hurfy, 896BC]
    r_comments = [i for comments in await gather(*tasks) for i in comments if isinstance(comments, list)]

    for comment in r_comments:
        comments.append(comment['body'])

    return {issue: {'Comments' : comments}}


@time_spent
async def gather_issues(session: object):
    """
    The function creates n-tasks to send requests for issues
    Then creates n-tasks to send requests for comments (issues)
    :param session: object: GitHub Session
    :return:          list: List of issues
    """
    tasks   = []
    issues  = {}
    total_p = await fetch_pages_count(session)

    # Creating tasks (issues)
    for page_index in range(1, total_p + 1):
        params = {"state": "all", "page": page_index, "per_page": 100}
        tasks.append(create_task(github_request(session, '/issues', params=params)))

    # Data acquisition and processing (issues) | Creating tasks (comments)
    issues_list = [i for issues in await gather(*tasks) for i in issues]
    tasks.clear()

    for issue in issues_list:
        number   = issue['number']
        cm_url   = issue['comments_url']
        cm_pages = ceil(issue['comments'] / 100)

        issues[number] = {'Name'        : issue['title'],
                          'Text'        : issue['body'],
                          'URL'         : issue['url'],
                          'Comments_URL': cm_url}

        url = cm_url.replace(fr'https://api.github.com/repos/{GITHUB_REPO}', '')
        tasks.append(create_task(gather_comments(session, url, cm_pages, number)))

    # Data acquisition and processing (comments)
    comments = {key: value for i in await gather(*tasks) for key, value in i.items()}

    for issue in issues:
        issues[issue].update(comments[issue])

    return issues
