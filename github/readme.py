from config   import GITHUB_TOKEN, GITHUB_REPO
from requests import get


def fetch_readme():
    """
    :return: str: README repository file if it exists, otherwise None
    """
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept'       : 'application/vnd.github.v3.raw'
    }
    url     = fr"https://api.github.com/repos/{GITHUB_REPO}/contents/README.md"
    readme  = get(url, headers=headers).text
    error   = r'{"message":"Not Found","documentation_url":' \
              r'"https://docs.github.com/rest/repos/contents#get-repository-content"}'

    return readme if readme != error else None


def save_to_storage(text: str):
    """
    Save README to .md file in storage
    :param text: str: Text to be written to a file
    :return:          None
    """
    with open('../storage/README.md', 'w', encoding='UTF-8', newline='') as md_file:
        md_file.write(text)
