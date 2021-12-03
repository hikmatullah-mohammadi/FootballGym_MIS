import sqlite3

# data base
class Database:
    def __init__(self):
        # create a connection
        self.conn = sqlite3.connect('gym.db')
        # create a cursor
        self.cursor = self.conn.cursor()
        # create customers table

        # self.cursor.execute('''CREATE TABLE customers
        #                     (name text,
        #                     ph_number text,
        #                     address text,
        #                     team_a text,
        #                     team_b text,
        #                     date text,
        #                     timing text,
        #                     payment integer
        #                     )
        #                     ''')

    # insert new records
    def insert_record(self, name, ph_number, address, team_a, team_b, date, timing, payment):
        self.cursor.execute('INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)'\
                            , (name, ph_number, address, team_a, team_b, date, timing, payment))
        self.conn.commit()


    def delete_record(self, id):
        self.cursor.execute('DELETE FROM customers WHERE rowid=?', (id, ))
        self.conn.commit()

    def all_records(self):
        self.cursor.execute('select * from customers')
        return self.cursor.fetchall()