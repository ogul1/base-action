import sys
import utils


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <yaml-file>")
        sys.exit(1)
    yaml_filename = sys.argv[1]
    file_content = utils.get_file_content(yaml_filename)
    utils.modify_file_content(file_content)


if __name__ == '__main__':
    main()
