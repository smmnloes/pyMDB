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
            DatabaseUpdateService.backup_last_version()
        elif user_input == 'restore':
            DatabaseUpdateService.restore_last_version()
        elif user_input == 'readbasics':
            DatabaseUpdateService.read_title_basisc()

main()
