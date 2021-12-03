from Database_class import Database
import unittest

class TestDatabaseMethods(unittest.TestCase):

    def setUp(self):
        self.my_database = Database()

    def test_insert_record(self):
        record = ('Hikmat', '0784840993', 'Kabul', 'Real', 'Barca', '15, 03, 21', '06:00-07:00 - AM', 5000)
        
        # insert a record
        self.my_database.insert_record('Hikmat', '0784840993', 'Kabul', 'Real', 'Barca', '15, 03, 21', '06:00-07:00 - AM', 5000)
        self.assertIn(record, self.my_database.all_records())
    
    def test_delete_record(self):
        id_to_delete = 3
        self.my_database.delete_record(id_to_delete)
        self.my_database.cursor.execute('SELECT rowid from customers')
        all_ids = []
        for id_ in self.my_database.cursor.fetchall():
            all_ids.append(id_[0])

        self.assertNotIn(id_to_delete, all_ids)


if __name__ == '__main__':
    unittest.main()