import sqlite3


def main():
    print("Hello world")

    readtitlebasisctodb()


def readtitlebasisctodb():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS 'title.basics'")
    c.execute(
        "CREATE TABLE 'title.basics' (tconst TEXT, primaryTitle TEXT, originalTitle TEXT, "
        "year INTEGER, runtimeMinutes INTEGER, genres TEXT)")

    with open('../DB Data/IMDB/title.basics.tsv', 'r') as file:
        line = file.readline()
        line = file.readline().strip()

        count = 1
        while line:
            entries = line.split('\t')

            if (entries[1] == "movie") & (entries[4] == "0"):
                del entries[1]
                del entries[3]
                del entries[4]
                c.execute("INSERT INTO 'title.basics' VALUES (?,?,?,?,?,?)", entries)

            line = file.readline().strip()
            print("Reading line %d" % count)
            count += 1

    conn.commit()
    conn.close()


main()
