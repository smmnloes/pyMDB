from DatabaseUpdateService import DatabaseUpdateService


def main():
    print("Welcome to Max' Movie Recommendation Engine!")
    dbupdate = DatabaseUpdateService()
    #dbupdate.read_title_basisc()
    dbupdate.download_new_data()


main()
