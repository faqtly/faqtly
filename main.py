from config  import GITHUB_TOKEN
from storage import PATH, readme_exists, issues_exist
from github  import fetch_repo_description
from os.path import exists
from os      import makedirs
from aiohttp import ClientSession
from asyncio import run


async def main():
    """
    Main function
    :return: None
    """
    if not exists(PATH):
        makedirs(PATH, exist_ok=True)

    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3.raw'
    }

    async with ClientSession(base_url=r'https://api.github.com', headers=headers) as session:
        description = await fetch_repo_description(session)
        readme      = await readme_exists(session)
        issues      = await issues_exist(session)

if __name__ == '__main__':
    run(main())
