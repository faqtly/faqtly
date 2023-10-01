from decouple import config
from github   import github
from json     import dump

GITHUB_TOKEN = config('GITHUB_TOKEN')
GITHUB_REPO  = config('GITHUB_REPO')
OPENAI_TOKEN = config('OPENAI_TOKEN')


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
    issues = github.fetch_issue(GITHUB_TOKEN, GITHUB_REPO)
    with open('output.json', 'w', encoding='UTF-8', newline='') as file:
        dump(issues, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    if validate_credits():
        main()
