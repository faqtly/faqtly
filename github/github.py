from config   import GITHUB_TOKEN, GITHUB_REPO
from requests import get, post
from math     import ceil
from re       import sub
from aiohttp  import ClientSession
from asyncio  import create_task, gather


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
