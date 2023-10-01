import requests


def fetch_readme(token, repo):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3.raw'

    }
    return requests.get(f"https://api.github.com/repos/{repo}/contents/README.md", headers=headers).text
