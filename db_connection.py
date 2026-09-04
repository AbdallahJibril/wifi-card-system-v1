import mysql.connector
class DBConnection:
    def __init__(self):
        self.my_con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="my_wi_fi"
        )
        self._current_cursor = None
    def cursor(self):
         self._current_cursor = self.my_con.cursor()
         return self._current_cursor
    def __enter__(self):
         return self
    def __exit__(self, exc_type, exc, tb):
        if self._current_cursor:
            try :
                self._current_cursor.close()
            except:
                pass
        if self.my_con:
            self.my_con.close()
    def commit(self):
        self.my_con.commit()

    # def close(self):
    #     self.my_con.close()
    
    