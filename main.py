from ui.Login import Window_login
from ui.Admin import Window_admin
import sys
import os
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
Password = "{str(self.login.lineEdit.text())}"
"""
                f.writelines(text + ''.join(text1))
        check = self.bd.check_pass(str(self.login.lineEdit.text()), str(self.login.lineEdit.text()))
        if check  == 2:
            print(1)
            self.login.close()
            self.admin = Window_admin()
            self.admin.show()
            print(2)

        else:
            QMessageBox.about(self, "Error", "Wrong Login or password")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainFrom()
    sys.exit(app.exec_())