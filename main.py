import sys
import utils
import os


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <yaml-file>")
        sys.exit(1)
    yaml_file_path = sys.argv[1]
    yaml_file_content = utils.get_file_content(yaml_file_path)

    modified_file = utils.modify_file_content(yaml_file_content)
    print(modified_file)

    open(".github/workflows/modified-workflow.yml", "w+").write(modified_file)


if __name__ == '__main__':
    main()
