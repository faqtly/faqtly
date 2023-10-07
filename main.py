from config   import GITHUB_TOKEN, GITHUB_REPO, OPENAI_TOKEN
from github   import github
from json     import dump, load
from os       import path, mkdir


# Primitive token validation
def validate_credits():
    """
    The function primitively checks the correctness of tokens entered by the user
    In case of problems will cause an error with a detailed description

    :return: bool: True
    """
    if GITHUB_TOKEN.startswith('<') or not GITHUB_TOKEN:
        raise Exception('Invalid or missing GITHUB_TOKEN in the .env file')

    if GITHUB_REPO.startswith('<')  or not GITHUB_REPO:
        raise Exception('Invalid or missing GITHUB_REPO in the .env file')

    if OPENAI_TOKEN.startswith('<') or not OPENAI_TOKEN:
        raise Exception('Invalid or missing OPENAI_TOKEN in the .env file')

    return True


def main():
    if not path.exists('storage'):
        mkdir('storage')

    # readme = github.fetch_readme(GITHUB_TOKEN, GITHUB_REPO)
    # issues = github.fetch_issue(GITHUB_TOKEN, GITHUB_REPO)

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
    if validate_credits():
        main()
