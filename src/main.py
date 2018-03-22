from threading import Thread

import requests

from DatabaseServices import Server, QueryService
from DatabaseServices import UpdateService

testquery_data = {"director": "Ron Howard",
                  "writer": "",
                  "year_from": "",
                  "year_to": "",
                  "genres": "",
                  "minRatingIMDB": 5.0}


def testquery_rest():
    url = "http://localhost:5002/query"
    requests.post(url, json=testquery_data)


def main():
    print("Welcome to Max' Movie Recommendation Engine!")
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
        elif user_input == 'startserver':
            thread = Thread(target=Server.start_app)
            thread.start()
        elif user_input == 'querylocal':
            result = QueryService.get_movies_by_criteria(testquery_data)
            for r in result:
                print(r)

        elif user_input == 'analyze':
            UpdateService.analyze()


main()
