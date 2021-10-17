from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from user_airsearch import * # 航班查询
from user_ordersearch import * # 订单查询
from user_ticketprint import * # 机票打印
from user_ticketunsubscribe import * # 机票退订
from user_airstatus import * # 航班预订情况
import sys, pymysql

class select_window(QWidget):
	'''
	服务选择界面
	'''
	def __init__(self):
		super().__init__()
		self.date = '2021年6月28日'
		self.initUI()
		self.connectdb()

	def initUI(self):
		'''
		初始化界面
		'''
		self.setFont(QFont("Arial",13))
		self.setWindowTitle('机票管理系统')
		self.resize(300, 300)
		self.setFixedSize(self.width(),self.height())

		# 总体竖直布局
		self.vbox = QVBoxLayout()

		# 日期
		self.lb3 = QLabel(self)
		self.lb3.setText(self.date)
		self.lb3.setAlignment(Qt.AlignCenter)
		self.vbox.addWidget(self.lb3)

		# 数据库连接状态
		self.lb4 = QLabel(self)
		self.lb4.setText('未连接数据库')
		self.lb4.setAlignment(Qt.AlignCenter)
		self.vbox.addWidget(self.lb4)

		self.bt1 = QPushButton('航班查询',self)
		self.bt2 = QPushButton('订单查询',self)
		self.bt3 = QPushButton('机票打印',self)
		self.bt4 = QPushButton('机票退订',self)
		self.bt5 = QPushButton('预订情况',self)
		self.bt6 = QPushButton('连接数据库',self)
		self.bt7 = QPushButton('退出',self)

		self.bt1.clicked.connect(self.AirSearch)
		self.bt2.clicked.connect(self.OrderSearch)
		self.bt3.clicked.connect(self.TicketPrint)
		self.bt4.clicked.connect(self.TicketUnsubscribe)
		self.bt5.clicked.connect(self.AirStatus)
		self.bt6.clicked.connect(self.connectdb)
		self.bt7.clicked.connect(qApp.quit)

		self.h1box = QHBoxLayout()
		self.h1box.addWidget(self.bt1)
		self.h1box.addWidget(self.bt2)
		self.h2box = QHBoxLayout()
		self.h2box.addWidget(self.bt3)
		self.h2box.addWidget(self.bt4)
		self.h3box = QHBoxLayout()
		self.h3box.addWidget(self.bt5)
		self.h3box.addWidget(self.bt6)
		self.vbox.addLayout(self.h1box)
		self.vbox.addLayout(self.h2box)
		self.vbox.addLayout(self.h3box)
		self.vbox.addWidget(self.bt7)

		self.setLayout(self.vbox)

	def check(self):
		'''
		检查数据库是否连接
		'''
		if self.bt6.isEnabled():
			return False
		else:
			return True

	def alert(self):
		'''
		连接数据库提醒
		'''
		QMessageBox.information(self,'提示','请先连接数据库！',QMessageBox.Ok)

	def AirSearch(self):
		'''
		航班查询
		'''
		if self.check():
			self.hide()
			self.airs = AirSearch()
			self.airs.show()
		else:
			self.alert()

	def OrderSearch(self):
		'''
		订单查询
		'''
		if self.check():
			self.hide()
			self.uo = user_ordersearch()
			self.uo.show()
		else:
			self.alert()

	def TicketPrint(self):
		'''
		机票打印
		'''
		if self.check():
			self.hide()
			self.tp = user_ticketprint()
			self.tp.show()
		else:
			self.alert()

	def TicketUnsubscribe(self):
		'''
		机票退订
		'''
		if self.check():
			self.hide()
			self.utu = user_ticket_unsubscribe()
			self.utu.show()
		else:
			self.alert()

	def AirStatus(self):
		'''
		航班预订情况
		'''

		if self.check():
			self.hide()
			self.astatus = user_airstatus()
			self.astatus.show()
		else:
			self.alert()


	def connectdb(self):
		'''
		连接数据库，选择界面的连接仅为后续作测试用，连接后关闭即可
		'''
		try:
			self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')
			self.lb4.setText('已连接数据库')
			self.bt6.setEnabled(False)

			self.airinfo.close()
		except:
			pass
