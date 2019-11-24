import sqlite3


class SQLLiter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database=database)
        self.cursor = self.connection.cursor()

    def fetch_all_records(self):
        return self.cursor.execute("SELECT * FROM music;").fetchall()

    def fetch_single_record(self, row_number):
        return self.cursor.execute("SELECT * FROM music WHERE id=?;", (row_number,)).fetchall()

    def count_rows(self):
        return self.cursor.execute("SELECT COUNT(*) FROM music;").fetchone()

    def close_connection(self):
        return self.connection.close()
