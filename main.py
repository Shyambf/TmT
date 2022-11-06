from ui.Login import Window_login
from ui.Admin import Window_admin
from ui.Edit_group import Window_group
import sys
import os
import time
from ui.sql_api import Bd
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox


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
        check = self.bd.check_pass(str(self.login.lineEdit.text()), str(self.login.lineEdit_2.text()))
        if check  == 2:
            self.admin_w(self.login)

        else:
            QMessageBox.about(self, "Error", "Wrong Login or password")
        
    def admin_w(self, last_window):
            last_window.close()
            self.admin = Window_admin()
            self.admin.show()
            self.addActions(self.admin)

    def create_new_group(self, window):
        window.close()
        self.add_group = Window_group()
        self.add_group.show()
        self.addActions(self.add_group)
        self.add_group.pushButton.clicked.connect(lambda:self.create_group(self.add_group))
    
    def create_group(self, window):
            name = self.add_group.lineEdit.text()
            num = self.add_group.spinBox.value()
            teacher = self.bd.get_id_by_teacher(self.add_group.comboBox.currentText())
            descript = self.add_group.textEdit.toPlainText()
            self.bd.add_group(name, descript, num, teacher)
            self.admin_w(window)


    def addActions(self, window):
        window.action_2.triggered.connect(lambda: self.create_new_group(window))
        window.action_4.triggered.connect(lambda: self.admin_w(window))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainFrom()
    sys.exit(app.exec_())