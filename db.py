import sqlite3


class DBHelper:

    def __init__(self, dbname="lizzy.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS userInfo (user_id INTEGER PRIMARY KEY NOT NULL, user_street text,user_radius INTEGER,user_category text)"
        #liststmt = "CREATE TABLE IF NOT EXISTS lastSavedList (user_id INTEGER PRIMARY KEY NOT NULL, user_street text)"
        self.conn.execute(tblstmt)
        #self.conn.execute(liststmt)
        self.conn.commit()

    def is_user_register(self, user_id):
        stmt = "SELECT * FROM userInfo WHERE user_id = (?)"
        args = (user_id,)
        user_check_data = [x[0] for x in self.conn.execute(stmt, args)]
        if not user_check_data:
            return False
        else:
            return True

    def register_user(self, user_id, user_street, user_radius, user_category):
        stmt = "SELECT * FROM userInfo WHERE user_id = (?)"
        args = (user_id,)
        user_check_data = [x[0] for x in self.conn.execute(stmt, args)]
        if not user_check_data:
            print("User not registered")
            stmt = "INSERT INTO userInfo (user_id, user_street,user_radius,user_category) VALUES (?, ?, ?, ?)"
            args = (user_id, user_street, user_radius, user_category)
            self.conn.execute(stmt, args)
            self.conn.commit()
        else:
            print("User registered")

    def get_user_street(self, user_id):
        stmt = "SELECT user_street FROM userInfo WHERE user_id = (?)"
        args = (user_id,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_user_radius(self, user_id):
        stmt = "SELECT user_radius FROM userInfo WHERE user_id = (?)"
        args = (user_id,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_user_category(self, user_id):
        stmt = "SELECT user_category FROM userInfo WHERE user_id = (?)"
        args = (user_id,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def update_user_category(self, user_id,user_category):
        stmt = "UPDATE userInfo SET user_category = (?) WHERE user_id = (?)"
        args = (user_category,user_id)
        self.conn.execute(stmt, args)
        self.conn.commit()
