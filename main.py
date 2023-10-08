from config          import GITHUB_TOKEN, GITHUB_REPO, OPENAI_TOKEN
from github.github   import fetch_issue
from github.readme   import fetch_readme
from json            import dump, load
from os.path         import exists
from os              import mkdir


def main():
    if not exists('storage'):
        mkdir('storage')

    # readme = fetch_readme()
    # issues = fetch_issue()

    # Write README to .md
    # with open(f'storage/README.md', 'w', encoding='UTF-8', newline='') as file:
    #     file.write(readme)

    # Load issues from .json [Temp]
    # with open(f'storage/{GITHUB_REPO}.json', 'r', encoding='UTF-8', newline='') as file:
    #     issues = load(file)

    # Write issues to .json
    # with open(f'storage/{GITHUB_REPO[GITHUB_REPO.find("/") + 1:]}.json', 'w', encoding='UTF-8', newline='') as file:
    #     dump(issues, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
