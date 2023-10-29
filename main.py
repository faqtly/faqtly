from config  import GITHUB_REPO, GITHUB_TOKEN
from github  import fetch_repo_description, fetch_readme, gather_issues
from json    import dump, load
from os.path import exists
from os      import makedirs
from aiohttp import ClientSession
from asyncio import run

# Each repository will have its own folder in the storage to avoid conflicts
PATH = fr'storage/{GITHUB_REPO[GITHUB_REPO.find("/") + 1:]}'
JSON = fr'{PATH}/{GITHUB_REPO[GITHUB_REPO.find("/") + 1:]}.json'
RDME = fr'{PATH}/README.md'


def load_file(file: str):
    """
    Function for reading data from local repository
    :param file:  str: Filename
    :return: list|str: File || dict - .json file (issues) || str - .txt file (README)
    """
    if file == 'issues':
        with open(JSON, 'r', encoding='UTF-8', newline='') as file:
            return load(file)

    if file == 'readme':
        with open(RDME, 'r', encoding='UTF-8', newline='') as file:
            return file.read()


def write_file(text: dict or str):
    """
    Function for writing data to local storage
    :param text: list|str: Type || dict - write to .json (issues) || str - write to .txt (README)
    :return:               None
    """
    if isinstance(text, dict):
        with open(JSON, 'w', encoding='UTF-8', newline='') as file:
            dump(text, file, ensure_ascii=False, indent=4)

    if isinstance(text, str):
        with open(RDME, 'w', encoding='UTF-8', newline='') as file:
            file.write(text)


async def readme_exists(session: object):
    """
    Primitive caching
    The function checks if a file exists in local storage
    :return: str: README.md file
    """
    if exists(RDME):
        return load_file('readme')

    readme = await fetch_readme(session)
    write_file(readme)

    return readme


async def issues_exist(session: object):
    """
    Primitive caching
    The function checks if a file exists in local storage
    :return: list: List of issues
    """
    if exists(JSON):
        return load_file('issues')

    issues = await gather_issues(session)
    write_file(issues)

    return issues


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
