from DatabaseUpdateService import DatabaseUpdateService


def main():
    print("Welcome to Max' Movie Recommendation Engine!")
    dbupdate = DatabaseUpdateService()
    dbupdate.update_db()


main()
