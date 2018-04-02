from threading import Thread

import requests

from App import AppMain
from DatabaseServices import QueryService
from DatabaseServices import UpdateService
from test.Testqueries import testquery_data


def testquery_rest():
    url = "http://localhost:5002/query"
    requests.post(url, json=testquery_data[5])


def main():
    print("Welcome to Max' Movie Recommendation Engine!")
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
        elif user_input == 'queryrest':
            testquery_rest()
        elif user_input == 'querylocal':
            result = QueryService.get_movies_by_criteria(testquery_data[5])
            for r in result:
                print(r)
        elif user_input == 'queryall':
            for query in testquery_data:
                print("\n\n\n" + str(query) + "\n")
                QueryService.get_movies_by_criteria(query)
        elif user_input == 'analyze':
            UpdateService.analyze()


main()
