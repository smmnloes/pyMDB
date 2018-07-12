from multiprocessing import Process

from App import AppMain
from DatabaseServices import UpdateService


def main():
    print("Welcome to pyMDB!")
    print("Starting App...")
    app_process = Process(target=AppMain.start_app)
    app_process.start()

    user_input = ''
    while user_input != 'exit':
        user_input = input('Please enter Command! (\'exit\' to quit)')

        if user_input == 'update':
            try:
                UpdateService.update_db()
            except (Exception, BaseException):
                break

        elif user_input == 'download':
            next_input = input('Download which dataset? ')
            UpdateService.download_and_unzip_new_data(next_input)
        elif user_input == 'backup':
            UpdateService.backup_local_db()
        elif user_input == 'restore':
            UpdateService.restore_db_last_version()
        elif user_input == 'read':
            next_input = input('Read which dataset? ')
            UpdateService.DATASETS_TO_READ_FUNCTIONS.get(next_input)()

    shutdown(app_process)


def shutdown(process):
    process.terminate()
    process.join()


if __name__ == '__main__':
    main()
