from github.github import github_request


async def fetch_readme(session: object):
    """
    Function to get README file of the repository
    :param session: object: GitHub Session
    :return:      str|None: README repository file if it exists, otherwise None
    """
    error    = r'{"message":"Not Found","documentation_url":' \
               r'"https://docs.github.com/rest/repos/contents#get-repository-content"}'

    response = await github_request(session, '/contents/README.md', fr='text')

    return response if response != error else None

# TODO: Processing the README.md file, getting key information
