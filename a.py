import utils

yaml_file_content = """
# This is a basic workflow to help you get started with Actions

name: CI

# Controls when the workflow will run
on:
  # Triggers the workflow on push or pull request events but only for the "main" branch
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: 3.7
      
      # Runs a single command using the runners shell
      - name: Run a one-line script
        run: echo Hello, world!

      # Runs a set of commands using the runners shell
      - name: Run a multi-line script
        run: |
          echo Add other actions to build,
          echo test, and deploy your project.
      
      - name: Run base action
        uses: ogul1/base-action@main
        with:
          yaml-file: .github/workflows/example.yml
"""

loaded_yaml = utils.load_yaml(yaml_file_content)
python_version = utils.get_python_version(loaded_yaml)

print(python_version)

f = utils.modify_file_content(yaml_file_content, python_version)
print(f)
