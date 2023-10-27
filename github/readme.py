from github.github import github_request
from aiohttp       import ClientSession


async def fetch_readme():
    """
    Function to get README file of the repository
    :return: str|None: README repository file if it exists, otherwise None
    """
    async with ClientSession() as session:
        error    = r'{"message":"Not Found","documentation_url":' \
                   r'"https://docs.github.com/rest/repos/contents#get-repository-content"}'

        response = await github_request(session, '/contents/README.md', r_format='text')

    return response if response != error else None

# TODO: Processing the README.md file, getting key information
