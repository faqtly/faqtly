from config  import OPENAI_TOKEN
from storage import load_file, write_file, JSON
from openai  import OpenAI


def get_answer(text: str):
    client = OpenAI(api_key=OPENAI_TOKEN)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": text}]
    )

    return completion.choices[0].message.content


def classify_issue(issue_id: int):
    try:
        issues = load_file("issues", f"../{JSON}")
        issue  = issues[str(issue_id)]
        prompt = (f'You will be provided with a description of the problem, and your task is to categorize'
                  f'its type as Bug, Issue, or Feature request (Feature):\n"{issue["Text"]}"')

    except FileNotFoundError:
        raise FileNotFoundError('The file was not found in the local storage. You need to scan the repository!')

    except KeyError:
        raise KeyError('Issue with this ID was not found!')

    if 'Type' in issue:
        return issue['Type']

    issue_type    = get_answer(prompt)
    issue['Type'] = issue_type

    write_file(issues, f"../{JSON}")

    return issue_type


print(classify_issue(802))