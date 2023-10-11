from config        import GITHUB_TOKEN, GITHUB_REPO, OPENAI_TOKEN
from github.issues import gather_issues
from github.readme import fetch_readme
from json          import dump, load
from os.path       import exists
from os            import makedirs
from asyncio       import run


async def main():

    # Each repository will have its own folder in the storage to avoid conflicts
    path = fr'storage/{GITHUB_REPO[GITHUB_REPO.find("/") + 1:]}'

    if not exists(path):
        makedirs(path, exist_ok=True)

    # readme = fetch_readme()
    issues = await gather_issues()

    # Write README to .md
    # with open(f'{path}/README.md', 'w', encoding='UTF-8', newline='') as file:
    #     file.write(readme)

    # Load issues from .json [Temp]
    # with open(f'{path}/{GITHUB_REPO}.json', 'r', encoding='UTF-8', newline='') as file:
    #     issues = load(file)

    # Write issues to .json
    with open(f'{path}/{GITHUB_REPO[GITHUB_REPO.find("/") + 1:]}.json', 'w', encoding='UTF-8', newline='') as file:
        dump(issues, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    run(main())
