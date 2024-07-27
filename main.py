import sys
import utils


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <yaml-file>")
        sys.exit(1)
    yaml_file_path = sys.argv[1]
    yaml_file_content = utils.get_file_content(yaml_file_path)

    loaded_yaml = utils.load_yaml(yaml_file_content)
    python_version = utils.get_python_version(loaded_yaml)

    utils.modify_file_content(yaml_file_content, python_version)


if __name__ == '__main__':
    main()
