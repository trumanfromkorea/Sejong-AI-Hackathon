import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic,QtWidgets
from PyQt5.QAxContainer import *
from PyQt5.QtGui import *
import pymysql
import pymysql.cursors

#form 선언
login_ui = uic.loadUiType("main_windows.ui")[0]
join_ui = uic.loadUiType("join_windows.ui")[0]
wrong_ui = uic.loadUiType("wrong_windows.ui")[0]

#db연결
db = pymysql.connect(host='127.0.0.1',
                     user='root',
                     password='0000',
                     db='4h',
                     charset='utf8')

#pymysql의 cursor오브젝트를 가져오는 것
cur = db.cursor()
global id #id 저장 전역변수

class Login(QMainWindow, login_ui):
    def __init__(self):
        super().__init__()
        self.setUI()

    def setUI(self):
        self.setupUi(self)
        self.button_member.clicked.connect(self.memberButtonClick)
        self.button_login.clicked.connect(self.loginButtonClick)

    def memberButtonClick(self):
        _Join.show() #회원가입 form띄우기

    def loginButtonClick(self):
        global id
        _id = self.input_id.toPlainText()
        _pw = self.input_pw.toPlainText()
        cur.execute("select id,pw from member")
        row = cur.fetchall()
        for r in row:
            if _id == r[0]:
                if _pw == r[1]:
                    id = r[0]
                    return self.correct()
                else:
                    return self.wrong()
        return self.wrong()

    def wrong(self):
        _Wrong.show()



class Join(QMainWindow, join_ui):
    def __init__(self):
        super().__init__()
        self.setUI()

    def setUI(self):
        self.setupUi(self)
        self.button_join.clicked.connect(self.joinButtonClick)

    def joinButtonClick(self):
        _id = self.input_id.toPlainText()
        _pw = self.input_pw.toPlainText()
        _name = self.input_name.toPlainText()
        _height = self.input_height.toPlainText()
        _weight = self.input_weight.toPlainText()
        _gender = '남성'
        if self.button_woman.isChecked():
            _gender = '여성'
        sql = "INSERT INTO member VALUES('{}','{}','{}','{}','{}','{}');".format(str(_id),str(_pw),str(_name),str(_gender),int(_height),int(_weight))
        cur.execute(sql)
        db.commit()
        _Join.close()

class Wrong(QMainWindow, wrong_ui):
    def __init__(self):
        super().__init__()
        self.setUI()

    def setUI(self):
        self.button_OK.clicked.connect(self.OKButtonClick)

    def OKButtonClick(self):
        _Wrong.close()

app = QApplication(sys.argv)
_Login = Login()
_Join = Join()
_Wrong = Wrong()

_Login.show()
app.exec_()
