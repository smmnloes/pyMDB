from threading import Thread

import requests

from DatabaseServices import Server
from DatabaseServices import UpdateService


def testquery():
    url = "http://localhost:5002/query"
    data = {"director": "Steven Spielberg", "year_from": 2000, "year_to": 2018, 'genres': ['Adventure', 'Sci-Fi']}
    requests.post(url, json=data)


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
        elif user_input == 'query':
            testquery()
        elif user_input == 'startserver':
            thread = Thread(target=Server.start_app)
            thread.start()


main()
