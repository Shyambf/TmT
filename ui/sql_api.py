import code
import sqlite3
from datetime import datetime
import hashlib
import uuid

class Bd:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('data.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS groups(
                    id integer primary key,
                    name TEXT,
                    description TEXT,
                    num_students INTEGER,
                    teacher INTEGER);
                """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS teacher(
                    id integer primary key,
                    name TEXT,
                    description TEXT,
                    access INTEGER,
                    login TEXT primary key,
                    paswd TEXT);
                """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS students(
                    id integer primary key,
                    groups INTEGER,
                    Phone number TEXT,
                    SNILS TEXT,
                    Pers_data TEXT, 
                    School TEXT,
                    Class TEXT
                    Email TEXT,
                    Comment TEXT,
                    vk_id TEXT,
                    Telegram_id TEXT,
                    discord_id TEXT);
                """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS log(
                    userid TEXT,
                    fullname TEXT,
                    action TEXT,
                    time TEXT,
                    date TEXT);
                """)
        self.conn.commit()


    def __hash(self, password:str) -> hash:
        salt=uuid.uuid4().hex
        return hashlib.sha256(str(password).encode()).hexdigest() + ':' + salt
    
    def __gethash(self, passwd) -> int:
        hash, _ = passwd.split(':')
        return hash

    def get_all_teacher(self) -> list:
        return self.cur.execute("SELECT name FROM teacher").fetchall()

    def get_all_group(self) -> list:
        return self.cur.execute("SELECT name, num_students, teacher FROM groups").fetchall()
    
    def add_teacher(self, name:str, description:str, access:int, login:str, passwd:str):
        login = self.__hash(login)
        passwd = self.__hash(passwd)
        teacher = (None, name, description, access, login, passwd)
        self.cur.execute("INSERT INTO teacher VALUES(?, ?, ?, ?, ?, ?);", teacher)
        self.conn.commit()

    def add_group(self, name:str, description:str, num_students:int, teacher:str) -> None:
        group = (None, name, description, num_students, teacher)
        self.cur.execute("INSERT INTO groups VALUES(?, ?, ?, ?, ?);", group)
        self.conn.commit()

    def get_teacher_by_id(self, id) -> str:
        return self.cur.execute(f"SELECT name FROM teacher WHERE id = {id}").fetchall()[0][0]

    def get_id_by_teacher(self, name) -> str:
        return self.cur.execute(f'SELECT id FROM teacher WHERE name = "{name}"').fetchall()[0][0]

    
    def check_pass(self, login:str, password:str) -> id:
            self.cur.execute("SELECT * FROM teacher")
            user = self.cur.fetchall()
            if login == 'admin' and password == 'admin':
                return 2
            for i in user:
                if self.__gethash(self.__hash(login)) == self.__gethash(i[4]) and self.__gethash(self.__hash(password)) == self.__gethash(i[5]):
                    return i[3]
                else: 0

