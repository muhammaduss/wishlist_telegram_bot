import sqlite3


class BotDatabase:

    def __init__(self, db_file_name):
        self.db = sqlite3.connect(db_file_name)
        self.cursor = self.db.cursor()

    # def auth_check(self, user_id):
    #     return bool(len(self.cursor.execute()))
    # def add_user:
    #     if ()