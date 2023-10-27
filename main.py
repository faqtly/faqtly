from config            import GITHUB_REPO
from github.issues     import gather_issues
from github.readme     import fetch_readme
from json              import dump, load
from os.path           import exists
from os                import makedirs
from asyncio           import run

# Each repository will have its own folder in the storage to avoid conflicts
PATH = fr'storage/{GITHUB_REPO[GITHUB_REPO.find("/") + 1:]}'
JSON = fr'{PATH}/{GITHUB_REPO[GITHUB_REPO.find("/") + 1:]}.json'
RDME = fr'{PATH}/README.md'


def load_file(file: str):
    """
    Function for reading data from local repository
    :param file: str: Filename
    :return: list|str File || list - .json file (issues) || str - .txt file (README)
    """
    if file == 'issues':
        with open(JSON, 'r', encoding='UTF-8', newline='') as file:
            return load(file)

    if file == 'readme':
        with open(RDME, 'r', encoding='UTF-8', newline='') as file:
            return file.read()


def write_file(text: list or str):
    """
    Function for writing data to local storage
    :param text: list|str: Type || list - write to .json (issues) || str - write to .txt (README)
    :return: None
    """
    if isinstance(text, list):
        with open(JSON, 'w', encoding='UTF-8', newline='') as file:
            dump(text, file, ensure_ascii=False, indent=4)

    if isinstance(text, str):
        with open(RDME, 'w', encoding='UTF-8', newline='') as file:
            file.write(text)


async def readme_exists():
    """
    Primitive caching
    The function checks if a file exists in local storage
    :return: str: README.md file
    """
    if exists(RDME):
        return load_file('readme')

    readme = await fetch_readme()
    write_file(readme)

    return readme


async def issues_exist():
    """
    Primitive caching
    The function checks if a file exists in local storage
    :return: list: List of issues
    """
    if exists(JSON):
        return load_file('issues')

    issues = await gather_issues()
    write_file(issues)

    return issues


async def main():
    """
    Main function
    :return: None
    """
    if not exists(PATH):
        makedirs(PATH, exist_ok=True)

    await readme_exists()
    await issues_exist()


if __name__ == '__main__':
    run(main())
