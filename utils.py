import os
import requests
import base64
import ruamel.yaml

yaml = ruamel.yaml.YAML()

owner = os.environ['GITHUB_REPOSITORY'].split('/')[0]
repo = os.environ['GITHUB_REPOSITORY'].split('/')[1]
token: str = os.environ['GITHUB_TOKEN']
base_api_url: str = "https://api.github.com"
headers: dict = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"
}


def get_file_content(yaml_file_path: str) -> str:
    url = f"{base_api_url}/repos/{owner}/{repo}/contents/{yaml_file_path}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.text)
    return base64.b64decode(response.json()['content']).decode('utf-8')


def load_yaml(yaml_file_content: str):
    return yaml.load(yaml_file_content)


def get_python_version(loaded_yaml) -> str:
    python_version = "3.10"
    for job_name in loaded_yaml["jobs"].keys():
        if "steps" not in loaded_yaml["jobs"][job_name]:
            continue
        for step in loaded_yaml["jobs"][job_name]["steps"]:
            if "uses" not in step or "actions/setup-python" not in step["uses"] or "with" not in step:
                continue
            if "python-version" in step["with"]:
                python_version = step["with"]["python-version"]
    return python_version


def add_set_up_python_and_dependencies(modified_file: str, indent: int, python_version: str) -> str:
    modified_file += " " * indent + "- uses: actions/setup-python@v5\n"
    modified_file += " " * (indent + 2) + "with:\n"
    modified_file += " " * (indent + 4) + f"python-version: '{python_version}'\n"
    modified_file += " " * indent + "- name: Install dependencies\n"
    modified_file += " " * (indent + 2) + "run: |\n"
    modified_file += " " * (indent + 4) + "python -m pip install --upgrade pip\n"
    modified_file += " " * (indent + 4) + "pip install pandas\n"
    modified_file += " " * (indent + 4) + "pip install numpy\n"
    modified_file += " " * indent + "- run: sudo apt update\n"
    modified_file += " " * indent + "- run: sudo apt install inotify-tools\n"
    modified_file += " " * indent + f"- run: inotifywait -dmr /home/runner/work/{owner}/{repo}/ --format '%T;%w;%f;%e' --timefmt '%T' -o /home/runner/inotify-logs.csv\n"
    return modified_file


def add_push_results_to_another_repository(modified_file: str) -> str:
    modified_file += "test\n"
    return modified_file


def get_indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def modify_file_content(yaml_file_content: str, python_version: str) -> str:
    modified_file = ""
    initial_file = yaml_file_content.split("\n")
    total_lines = len(initial_file)
    steps_indent = -1

    for i, line in enumerate(initial_file):
        modified_file += line
        modified_file += "\n"

        if line.strip() == "" or line.lstrip()[0] == "#":  # empty line or comment line
            continue

        line_indent = get_indent(line)

        if "steps" in line:  # steps start
            steps_indent = line_indent
            indent = 0
            for j in range(i + 1, total_lines):
                if initial_file[j].strip() != "" and initial_file[j].lstrip()[0] != "#":
                    indent = get_indent(initial_file[j])
                    break
            modified_file = add_set_up_python_and_dependencies(modified_file, indent, python_version)

        if line_indent <= steps_indent and line.lstrip()[0] != '-':  # steps end
            # add code to collect the logs
            modified_file = add_push_results_to_another_repository(modified_file)

    print(modified_file)

    return modified_file
