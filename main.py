from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from ui.Login import Window_login
from ui.Admin import Window_admin
from ui.Edit_group import Window_group
from ui.Group import Window_new_group
from ui.Student import Window_student
from ui.Add_user import Window_add_user
from ui.Bot import Window_bot
from ui.sql_api import Bd
import time
import sys
import os


class MainFrom(QWidget):
    def __init__(self):
        super(MainFrom, self).__init__()
        self.bd = Bd()
        self.dir = os.path.abspath(os.curdir)
        self.login = Window_login()
        self.login.pushButton.clicked.connect(self.login_action)
        self.login.show()

    def login_action(self):
        if self.login.checkBox.isChecked():
            with open('.env', 'r+') as f:
                text1 = f.readlines()[2:]
                f.seek(0)
                text = f"""Login = "{str(self.login.lineEdit.text())}"
Password = "{str(self.login.lineEdit_2.text())}"
"""
                f.writelines(text + ''.join(text1))
        check = self.bd.check_pass(
            str(self.login.lineEdit.text()),
            str(self.login.lineEdit_2.text())
            )
        if check == 2:
            self.admin_w(self.login)
            self.check = 2
        elif check == 1:
            self.check = 1
            pass
        else:
            QMessageBox.about(self, "Error", "Wrong Login or password")

    def admin_w(self, last_window):
        last_window.close()
        self.admin = Window_admin()
        for i in self.bd.get_all_group():
            self.admin.comboBox.addItem(i[1])
        name = self.admin.comboBox.currentText()
        id = self.bd.get_group_id_by_name(name)[0]
        self.admin.pushButton_2.clicked.connect(
            lambda: self.view_group(windows=self.admin, ids=id)
            )
        self.admin.show()
        self.addActions(self.admin)

    def view_group(self, windows, ids):
        windows.close()
        self.view_one_group = Window_new_group(ids)
        self.view_one_group.pushButton_4.clicked.connect(
            lambda: self.admin_w(self.view_one_group)
            )
        name = self.view_one_group.comboBox_2.currentText()
        id = self.bd.get_student_by_name(name)
        self.view_one_group.pushButton_2.clicked.connect(
            lambda: self.user_w(
                window=self.view_one_group, ids=id[0], group=ids
                )
            )
        self.addActions(self.view_one_group)
        self.view_one_group.pushButton.clicked.connect(
            lambda: self.edit_group(self.view_one_group, id))
        self.view_one_group.pushButton_3.clicked.connect(
            lambda: self.bot(self.view_one_group, ids)
            )
        self.view_one_group.show()

    def create_new_group(self, window):
        window.close()
        self.add_group = Window_group()
        self.add_group.show()
        self.addActions(self.add_group)
        self.add_group.pushButton.clicked.connect(
            lambda: self.create_group(self.add_group))

    def edit_group(self, window, id):
        name = window.lineEdit.text()
        num_students = window.spinBox.value()
        teacher = self.bd.get_id_by_teacher(
            window.comboBox.currentText()
            )
        description = window.lineEdit_2.text()
        self.bd.edit_group(id, name, description, num_students, teacher)
        QMessageBox.about(self, "Успешно", "Данные группы изменены")

    def create_group(self, window):
        name = self.add_group.lineEdit.text()
        num = self.add_group.spinBox.value()
        teacher = self.bd.get_id_by_teacher(
            self.add_group.comboBox.currentText()
            )
        descript = self.add_group.textEdit.toPlainText()
        self.bd.add_group(name, descript, num, teacher)
        self.admin_w(window)

    def user_w(self, window, group, ids=None):
        window.close()
        self.user = Window_student(id=ids, flag=True)
        self.addActions(self.user)
        self.user.show()
        self.user.pushButton.clicked.connect(self.user.save)
        self.user.pushButton_2.clicked.connect(
            lambda: self.view_group(windows=self.user, ids=group)
            )

    def add_user(self, window):
        window.close()
        self.ad_user = Window_add_user()
        self.addActions(self.ad_user)
        self.ad_user.show()

    def bot(self, window, group):
        window.close()
        self.bots = Window_bot(group)
        self.bots.show()
        self.bots.pushButton_2.clicked.connect(
            lambda: self.view_group(self.bots, group)
            )

    def addActions(self, window):
        window.action_2.triggered.connect(
            lambda: self.create_new_group(window)
            )
        window.action_4.triggered.connect(
            lambda: self.admin_w(window)
            )
        window.action_3.triggered.connect(
            lambda: self.add_user(window)
            )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainFrom()
    sys.exit(app.exec_())
