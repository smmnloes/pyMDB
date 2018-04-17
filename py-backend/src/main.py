from threading import Thread

from App import AppMain
from DatabaseServices import QueryService
from DatabaseServices import UpdateService
from test.Testqueries import testquery_data


def main():
    print("Welcome to pyMDB!")
    print("Starting App...")
    thread = Thread(target=AppMain.start_app)
    thread.start()

    user_input = ''
    while user_input != 'exit':
        user_input = input('Please enter Command! ')

        if user_input == 'update':
            UpdateService.update_db()
        elif user_input == 'download':
            next_input = input('Download which dataset? ')
            UpdateService.download_new_data(next_input)
        elif user_input == 'backup':
            UpdateService.backup_local_db()
        elif user_input == 'restore':
            UpdateService.restore_db_last_version()
        elif user_input == 'read':
            next_input = input('Read which dataset? ')
            UpdateService.DATASETS_TO_READ_FUNCTIONS.get(next_input)()
        elif user_input == 'queryall':
            i = 1
            for query in testquery_data:
                print('#{}'.format(i))
                QueryService.get_movies_by_criteria(query)
                i += 1

main()
