import sqlite3


class DB:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connectDB()

    def connectDB(self):
        if self.conn is None:
            try:
                self.conn = sqlite3.connect('inverted-index.db')
                self.cur = self.conn.cursor()
            except sqlite3.Error as error:
                print(error)

    def disconnectDB(self):
        if self.conn:
            self.conn.close()
        if self.cur:
            self.cur.close()

    def createTable(self):
        self.cur.execute('''
            CREATE TABLE IndexWord (
                word TEXT PRIMARY KEY
            );
        ''')
        self.cur.execute('''
            CREATE TABLE Posting (
                word TEXT NOT NULL,
                documentName TEXT NOT NULL,
                frequency INTEGER NOT NULL,
                indexes TEXT NOT NULL,
                PRIMARY KEY(word, documentName),
                FOREIGN KEY (word) REFERENCES IndexWord(word)
                );
        ''')
        self.conn.commit()




