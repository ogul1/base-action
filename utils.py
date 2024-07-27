import os
import requests
import base64

token = os.environ['GITHUB_TOKEN']
base_api_url: str = "https://api.github.com"
headers: dict = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"
}


def get_file_content(file_path):
    url = f"{base_api_url}/repos/{os.environ['GITHUB_REPOSITORY']}/contents/{file_path}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.text)
    return base64.b64decode(response.json()['content']).decode('utf-8')


def modify_file_content(file_content):
    print(file_content)
