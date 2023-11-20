from config  import GITHUB_REPO
from json    import dump, load
from os.path import exists
from github  import fetch_readme, gather_issues


# Each repository will have its own folder in the storage to avoid conflicts
PATH = fr'storage/{GITHUB_REPO[GITHUB_REPO.find("/") + 1:]}'
JSON = fr'{PATH}/{GITHUB_REPO[GITHUB_REPO.find("/") + 1:]}.json'
RDME = fr'{PATH}/README.md'


def load_file(f_type: str, path: str):
    """
    Function for reading data from local repository
    :param f_type: str: Filetype
    :param path:   str: Filepath
    :return:  list|str: File || dict - .json file (issues) || str - .txt file (README)
    """
    if f_type == 'issues':
        with open(path, 'r', encoding='UTF-8', newline='') as file:
            return load(file)

    if f_type == 'readme':
        with open(path, 'r', encoding='UTF-8', newline='') as file:
            return file.read()


def write_file(text: dict or str, path: str):
    """
    Function for writing data to local storage
    :param path:      str: Filepath
    :param text: list|str: Type || dict - write to .json (issues) || str - write to .txt (README)
    :return:               None
    """
    if isinstance(text, dict):
        with open(path, 'w', encoding='UTF-8', newline='') as file:
            dump(text, file, ensure_ascii=False, indent=4)

    if isinstance(text, str):
        with open(path, 'w', encoding='UTF-8', newline='') as file:
            file.write(text)


async def readme_exists(session: object):
    """
    Primitive caching
    The function checks if a file exists in local storage
    :return: str: README.md file
    """
    if exists(RDME):
        return load_file('readme', RDME)

    readme = await fetch_readme(session)
    write_file(readme, RDME)

    return readme


async def issues_exist(session: object):
    """
    Primitive caching
    The function checks if a file exists in local storage
    :return: list: List of issues
    """
    if exists(JSON):
        return load_file('issues', JSON)

    issues = await gather_issues(session)
    write_file(issues, JSON)

    return issues
