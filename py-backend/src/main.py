import getopt
import sys

from App import AppMain
from Services.Database import UpdateService


def main(argv):
    print("Welcome to pyMDB!")
    print("Parsing command line arguments...")
    parse_arguments(argv)
    print("Starting App...")
    AppMain.start_app()


def parse_arguments(argv):
    try:
        opts, args = getopt.getopt(argv, "update", [])
    except getopt.GetoptError:
        return

    for arg in args:
        if arg == "update":
            print("Updating database...")
            AppMain.create_app()
            UpdateService.update_db()
            exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
