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
                    id integer primary key AUTOINCREMENT,
                    name TEXT,
                    description TEXT,
                    num_students INTEGER,
                    teacher TEXT);
                """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS teacher(
                    id integer primary key,
                    name TEXT,
                    description TEXT,
                    login TEXT,
                    pass TEXT);
                """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS students(
                    id integer primary key AUTOINCREMENT,
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


    def __hash(password:int, salt=uuid.uuid4().hex) -> hash:
        # uuid используется для генерации случайного числа
        return hashlib.sha256(salt.encode() + str(password).encode()).hexdigest() + ':' + salt
    
    def __unhash(passwd):
        _, salt = passwd.split(':')
        return salt

    def get_all_group(self) -> list:
        return self.cur.execute("SELECT name, num_students, teacher FROM groups")

    def add_group(self, name:str, description:str, num_students:int, teacher:str) -> None:
        group = (None, name, description, num_students, teacher)
        self.cur.execute("INSERT INTO groups VALUES(?, ?, ?, ?, ?);", group)
        self.conn.commit()

    def add_teacher(self, name:str, description:str, login:str, password:str) -> None:
        teacher = (name, description, self.__hash(login), self.__hash(password))
        self.cur.execute("INSERT INTO log VALUES(?, ?, ?, ?);", teacher)
        self.conn.commit()
    
    def check_pass(self, login:str, password:str) -> id:
            self.cur.execute("SELECT * FROM teacher")
            user = self.cur.fetchall()
            if login == 'admin' and password == 'admin':
                return 2
            for i in user:
                salt = self.__unhash(i[3])
                if hash(login, salt) == i[3] and hash(password, salt) == i[4]:
                    return 1
                else: 0

