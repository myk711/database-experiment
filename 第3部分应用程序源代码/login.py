from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from passwords import * # 用户管理员账号密码
from user_select import * # 用户选择界面
import sys

class login(QDialog):
	'''
	登录界面
	'''
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setFont(QFont("Arial",14))
		self.setWindowTitle('登录')
		self.resize(350,200)
		self.setFixedSize(self.width(),self.height())

		# 总体竖直布局
		self.vbox = QVBoxLayout()

		# 打个招呼
		self.lb = QLabel('机票预订系统',self)
		self.lb.setAlignment(Qt.AlignCenter)
		self.vbox.addWidget(self.lb)


		# 用户名
		self.user = QLineEdit(self)
		self.user.setPlaceholderText('请输入用户名')
		self.vbox.addWidget(self.user)

		# 密码
		self.password = QLineEdit(self)
		self.password.setPlaceholderText('请输入密码')
		self.password.setEchoMode(QLineEdit.Password)
		self.vbox.addWidget(self.password)

		# 选项
		self.bt1 = QPushButton('确定',self)
		self.bt2 = QPushButton('退出',self)
		self.hbox2 = QHBoxLayout()
		self.hbox2.addWidget(self.bt1)
		self.hbox2.addWidget(self.bt2)
		self.vbox.addLayout(self.hbox2)
		
		# 总体水平布局
		self.hbox = QHBoxLayout()
		self.hbox.addLayout(self.vbox)
		self.setLayout(self.hbox)
		
		# 事件关联
		self.bt1.clicked.connect(self.confirm)
		self.bt2.clicked.connect(self.cancel)

	def confirm(self):
		self.ct1 = self.user.text()
		self.ct2 = self.password.text()

		if [self.ct1,self.ct2] in users : #用户
			self.hide()
			self.us = select_window()
			self.us.show()

		else: #账号或密码错误
			self.reply = QMessageBox.information(self,'提示','用户名或密码错误!',QMessageBox.Ok)
			if self.reply == QMessageBox.Ok:
				return

	def cancel(self):
		self.done(0)


