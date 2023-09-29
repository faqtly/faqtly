from github import Github
from dotenv import load_dotenv
from os import getenv

load_dotenv()
GITHUB_TOKEN = getenv('GITHUB_TOKEN')
GITHUB_REPO  = getenv('GITHUB_REPO')
OPENAI_TOKEN = getenv('OPENAI_TOKEN')


# Primitive token validation
def validate_credits():
    """
    The function primitively checks the correctness of tokens entered by the user
    In case of problems will cause an error with a detailed description

    :return: bool: True
    """
    if GITHUB_TOKEN.startswith('<') or GITHUB_TOKEN == '':
        raise Exception('Invalid or missing GITHUB_TOKEN in the .env file')

    if GITHUB_REPO.startswith('<') or GITHUB_REPO == '':
        raise Exception('Invalid or missing GITHUB_REPO in the .env file')

    if OPENAI_TOKEN.startswith('<') or OPENAI_TOKEN == '':
        raise Exception('Invalid or missing OPENAI_TOKEN in the .env file')

    return True


def main():
    git = Github()  # !!! Specify the token as an argument in the future [GITHUB_TOKEN] !!!
    repository = git.get_repo(GITHUB_REPO)

    issues = repository.get_issues()

    for issue in issues:
        print(f'Issue: {issue.title}({issue.state}) #{issue.user.login}',
              f'Text : {issue.body}', sep='\n')


if __name__ == '__main__':
    if validate_credits():
        main()

