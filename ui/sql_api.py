import hashlib
import sqlite3
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
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS teacher(
                    id integer primary key,
                    name TEXT,
                    description TEXT,
                    access INTEGER,
                    login TEXT UNIQUE,
                    paswd TEXT);
                """)
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS students(
                    id integer primary key,
                    groups INTEGER,
                    name TEXT,
                    Phone_number TEXT,
                    SNILS TEXT,
                    Pers_data TEXT,
                    School TEXT,
                    Class TEXT,
                    Email TEXT,
                    Comment TEXT,
                    vk_id TEXT NULL,
                    Telegram_id TEXT NULL,
                    discord_id TEXT NULL);
                """)
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS log(
                    userid TEXT,
                    fullname TEXT,
                    action TEXT,
                    time TEXT,
                    date TEXT);
                """)
        self.conn.commit()

    def __hash(self, password: str) -> hash:
        salt = uuid.uuid4().hex
        return hashlib.sha256(str(password).encode()).hexdigest() + ':' + salt

    def __gethash(self, passwd) -> int:
        hash, _ = passwd.split(':')
        return hash

    def get_all_teacher(self) -> list:
        return self.cur.execute("SELECT name FROM teacher").fetchall()

    def get_all_group(self) -> list:
        return self.cur.execute(
            "SELECT id, name, num_students, teacher FROM groups"
            ).fetchall()

    def get_all_group_teacher(self, id) -> list:
        return self.cur.execute(
            "SELECT id, name, num_students, teacher FROM \
                groups WHERE id = (?)",
            (id,)
            ).fetchall()

    def add_teacher(self, nam: str, desc: str, acc: int, login: str, pss: str):
        login = self.__hash(login)
        passwd = self.__hash(pss)
        teacher = (None, nam, desc, acc, login, passwd)
        self.cur.execute(
            "INSERT INTO teacher VALUES(?, ?, ?, ?, ?, ?);",
            teacher
        )
        self.conn.commit()

    def get_net_id_group(self, group):
        return self.cur.execute(
            f"SELECT vk_id, Telegram_id FROM students WHERE groups = {group}"
        ).fetchall()

    def add_group(self, name: str, desc: str, num: int, teacher: str) -> None:
        group = (None, name, desc, num, teacher)
        self.cur.execute("INSERT INTO groups VALUES(?, ?, ?, ?, ?);", group)
        self.conn.commit()

    def get_teacher_by_id(self, id: int):
        return self.cur.execute(
            "SELECT name FROM teacher WHERE id = (?)", (id,)
        ).fetchone()[0]

    def get_id_by_teacher(self, name) -> str:
        return self.cur.execute(
            f'SELECT id FROM teacher WHERE name = "{name}"'
        ).fetchone()[0]

    def get_group_by_id(self, id: int) -> list:
        return self.cur.execute(
            f'SELECT * FROM groups WHERE id = {id}'
        ).fetchone()

    def get_all_students_group(self, id) -> list:
        return self.cur.execute(
            'SELECT id, name FROM students WHERE groups = (?)',
            (id,)
        ).fetchall()

    def get_group_id_by_name(self, name):
        return self.cur.execute(
            f"SELECT id FROM groups WHERE name = (?)", (name,)
        ).fetchone()

    def add_student(
            self,
            groups,
            name,
            Phone_number,
            SNILS,
            Pers_data,
            School,
            Class,
            Email,
            Comment,
            vk_id,
            Telegram_id,
            discord_id):
        student = (
            None,
            groups,
            name,
            Phone_number,
            SNILS,
            Pers_data,
            School,
            Class,
            Email,
            Comment,
            vk_id,
            Telegram_id,
            discord_id)
        self.cur.execute(
            "INSERT INTO students \
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            student
        )
        self.conn.commit()

    def check_pass(self, login: str, password: str) -> id:
        self.cur.execute("SELECT * FROM teacher")
        user = self.cur.fetchall()
        if login == 'admin' and password == 'admin':
            return [2, 2]
        flag = False
        for i in user:
            if self.__gethash(self.__hash(login)) == self.__gethash(i[4]) and \
             self.__gethash(self.__hash(password)) == self.__gethash(i[5]):
                flag = True
                return [i[3], i[0]]
            else:
                pass
        if not flag:
            return 0

    def get_teacher_groups(self, id):
        return self.cur.execute(
            f"SELECT name FROM groups WHERE teacher = (?)", (id,)
        ).fetchall()

    def update_student_info(
        self,
        groups,
        name,
        Phone_number,
        SNILS, Pers_data,
        School,
        Class,
        Email,
        Comment,
        vk_id,
        Telegram_id,
        discord_id,
        id=0
    ):
        student = (
            groups,
            name,
            Phone_number,
            SNILS, Pers_data,
            School,
            Class,
            Email,
            Comment,
            vk_id,
            Telegram_id,
            discord_id
        )
        self.cur.execute(
            f"""UPDATE students
            SET
            id = {id},
            groups = ?,
            name = ?,
            Phone_number = ?,
            SNILS = ?,
            Pers_data = ?,
            School = ?,Class = ?,
            Email = ?,
            Comment = ?,
            vk_id = ?,
            Telegram_id = ?,
            discord_id = ?
            WHERE id = {id}
            """, (student))
        self.conn.commit()

    def get_student_by_name(self, name):
        return self.cur.execute(
            "SELECT id FROM students WHERE name = (?)",
            (name,)
        ).fetchone()

    def get_student_by_id(self, id):
        return self.cur.execute(
            "SELECT * FROM students WHERE id = (?)",
            (id,)
            ).fetchone()

    def edit_group(self, id, name, description, num_students, teacher):
        self.cur.execute(
            "UPDATE groups SET name = ?, description = ?, num_students = ?, \
            teacher = ? WHERE id = ?",
            (name, description, int(num_students), int(teacher), id)
        )
        self.conn.commit()

    def delete_group(self, group):
        self.cur.execute("DELETE FROM groups WHERE id = (?);", (group,))
        self.conn.commit()

    def delete_teacher(self, id):
        self.cur.execute("DELETE FROM teacher WHERE id = (?);", (id,))
        self.conn.commit()
