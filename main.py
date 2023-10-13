from config        import GITHUB_TOKEN, GITHUB_REPO, OPENAI_TOKEN
from github.issues import gather_issues
from github.readme import fetch_readme
from json          import dump, load
from os.path       import exists
from os            import makedirs
from asyncio       import run

# Each repository will have its own folder in the storage to avoid conflicts
path = fr'storage/{GITHUB_REPO[GITHUB_REPO.find("/") + 1:]}'
json = fr'{path}/{GITHUB_REPO[GITHUB_REPO.find("/") + 1:]}.json'
rdme = fr'{path}/README.md'


def load_file(file: str):
    if file == 'issues':
        with open(json, 'r', encoding='UTF-8', newline='') as file:
            return load(file)

    if file == 'readme':
        with open(rdme, 'r', encoding='UTF-8', newline='') as file:
            return file.read()


def write_file(text: list or str):
    if isinstance(text, list):
        with open(json, 'w', encoding='UTF-8', newline='') as file:
            dump(text, file, ensure_ascii=False, indent=4)

    if isinstance(text, str):
        with open(rdme, 'w', encoding='UTF-8', newline='') as file:
            file.write(text)


def readme_exists():
    if exists(rdme):
        return load_file('readme')

    readme = fetch_readme()
    write_file(readme)

    return readme


async def issues_exist():
    if exists(json):
        return load_file('issues')

    issues = await gather_issues()
    write_file(issues)

    return issues


async def main():
    if not exists(path):
        makedirs(path, exist_ok=True)

    readme = readme_exists()
    issues = await issues_exist()


if __name__ == '__main__':
    run(main())
