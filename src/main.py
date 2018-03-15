import sqlite3


def main():
    print("Hello world")

    readtitlebasisctodb(True, False)


def readtitlebasisctodb(only_movies, with_adult):
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS 'title.basics'")
    c.execute(
        "CREATE TABLE 'title.basics' (tconst TEXT, titleType TEXT, primaryTitle TEXT, originalTitle TEXT, "
        "isAdult INTEGER, startYear INTEGER, endYear INTEGER, runtimeMinutes INTEGER, genres TEXT)")

    with open('../DB Data/IMDB/title.basics.tsv', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        count = 1
        while line:
            entries = line.split('\t')

            if ((not only_movies) | (entries[1] == "movie")) & (with_adult | (entries[4] == "0")):
                c.execute("INSERT INTO 'title.basics' VALUES (?,?,?,?,?,?,?,?,?)", entries)

            line = file.readline().strip()
            print("Reading line %d" % count)
            count += 1

    conn.commit()
    conn.close()


main()
