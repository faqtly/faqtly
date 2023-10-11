from config        import GITHUB_TOKEN, GITHUB_REPO, OPENAI_TOKEN
from github.github import gather_issues
from github.issues import fetch_issue
from github.readme import fetch_readme
from json          import dump, load
from os.path       import exists
from os            import mkdir
from asyncio       import run


def main():

    # Each repository will have its own folder in the storage to avoid conflicts
    path = fr'{GITHUB_REPO[GITHUB_REPO.find("/") + 1:]}\storage'

    if not exists(path):
        mkdir(path)

    readme = fetch_readme()
    # issues = run(gather_issues())

    # Write README to .md
    with open(f'{path}/README.md', 'w', encoding='UTF-8', newline='') as file:
        file.write(readme)

    # Load issues from .json [Temp]
    # with open(f'{path}/{GITHUB_REPO}.json', 'r', encoding='UTF-8', newline='') as file:
    #     issues = load(file)

    # Write issues to .json
    # with open(f'{path}/{GITHUB_REPO[GITHUB_REPO.find("/") + 1:]}.json', 'w', encoding='UTF-8', newline='') as file:
    #     dump(issues, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
