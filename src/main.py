import DatabaseUpdateService


def main():
    print("Welcome to Max' Movie Recommendation Engine!")
    user_input = ''
    while user_input != 'exit':
        user_input = input('Please enter Command! ')

        if user_input == 'update':
            DatabaseUpdateService.update_db()
        elif user_input == 'download':
            DatabaseUpdateService.download_new_data('ratings')
        elif user_input == 'backup':
            DatabaseUpdateService.backup_local_db()
        elif user_input == 'restore':
            DatabaseUpdateService.restore_db_last_version()
        elif user_input == 'readbasics':
            DatabaseUpdateService.read_basics()
        elif user_input == 'readratings':
            DatabaseUpdateService.read_ratings()
        elif user_input == 'readakas':
            DatabaseUpdateService.read_akas()
        elif user_input == 'readprincipals':
            DatabaseUpdateService.read_principals()
        elif user_input == 'readcrew':
            DatabaseUpdateService.read_crew()
        elif user_input == 'readnames':
            DatabaseUpdateService.read_names()


main()
