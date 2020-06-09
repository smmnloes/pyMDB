import getopt
import sys

from app import app_main
from services.database import update_service


def main(argv):
    print("Welcome to pyMDB!")
    print("Parsing command line arguments...")
    parse_arguments(argv)
    print("Starting App...")
    app_main.start_app()


def parse_arguments(argv):
    try:
        opts, args = getopt.getopt(argv, "update", [])
    except getopt.GetoptError:
        return

    for arg in args:
        if arg == "update":
            print("Updating database...")
            app_main.create_app()
            update_service.update_db()
            exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
