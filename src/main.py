from DatabaseServices import DatabaseUpdateService
from DatabaseServices import Server


def main():
    print("Welcome to Max' Movie Recommendation Engine!")
    user_input = ''
    while user_input != 'exit':
        user_input = input('Please enter Command! ')

        if user_input == 'update':
            DatabaseUpdateService.update_db()
        elif user_input == 'download':
            next_input = input('Download which dataset? ')
            DatabaseUpdateService.download_new_data(next_input)
        elif user_input == 'backup':
            DatabaseUpdateService.backup_local_db()
        elif user_input == 'restore':
            DatabaseUpdateService.restore_db_last_version()
        elif user_input == 'read':
            next_input = input('Read which dataset? ')
            DatabaseUpdateService.DATASETS_TO_READ_FUNCTIONS.get(next_input)()
        elif user_input == 'query':
            movie = Server.Movie()
            result = movie.get("Steven Spielberg", 1900, 2018)
            print(result)


main()
