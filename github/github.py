from config import GITHUB_REPO
from re     import sub


async def github_request(session: object, url: str, fr: str = 'json', params: dict = None):
    """
    Function for sending requests to the GitHub API
    :param session: object: GitHub Session
    :param url:        str: Page URL
    :param fr:         str: Format || json - request.json() || other - request.text()
    :param params:    dict: Request params
    :return:      dict|str: Response
    """
    url = fr'/repos/{GITHUB_REPO}{url}'

    async with session.get(url, params=params) as response:
        response = await response.json() if fr == 'json' else await response.text()

    return response


async def fetch_repo_description(session: object):
    """
    Function to get repository description
    :return: str|None: Repository description
    """
    response = await github_request(session, '')

    # Convert description to plain text, removes unnecessary characters. Thanks a lot, Inlife! :D
    if (description := response['description']) is not None:
        description = sub(r'[^a-zA-Zа-яА-Я0-9\s.,!?-]', '', description).strip()

    return description
