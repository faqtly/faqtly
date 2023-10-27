from config   import GITHUB_TOKEN, GITHUB_REPO
from re       import sub
from aiohttp  import ClientSession


async def github_request(session: object, path: str, r_format: str = 'json', params: dict = None):
    """
    Function for sending requests to the GitHub API
    :param session: object: Async session
    :param path:       int: Page URL
    :param r_format:   str: Format || json - request.json() || other - request.text()
    :param params:    dict: Request params
    :return:      dict|str: Response
    """
    base_url = f'https://api.github.com/repos/{GITHUB_REPO}'
    url      = path if base_url in path else f'{base_url}{path}'

    headers  = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3.raw'
    }

    async with session.get(url, headers=headers, params=params) as response:
        response = await response.json() if r_format == 'json' else await response.text()

    return response


async def fetch_repo_description():
    """
    Function to get repository description
    :return: str|None: Repository description
    """
    async with ClientSession() as session:
        response = await github_request(session, fr'https://api.github.com/repos/{GITHUB_REPO}')

        # Convert description to plain text, removes unnecessary characters. Thanks a lot, Inlife! :D
        if description := response['description'] is not None:
            description = sub(r'[^a-zA-Zа-яА-Я0-9\s.,!?-]', '', description).strip()

    return description
