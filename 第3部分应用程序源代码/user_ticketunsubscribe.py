from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import user_select # 用户选择界面
import sys, pymysql

class user_ticket_unsubscribe(QMainWindow):
	'''
	机票退订页面
	'''
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		'''
		初始化界面
		'''
		self.setFont(QFont("Arial",12))
		self.resize(270,305)
		self.setFixedSize(self.width(),self.height())
		self.setWindowTitle('机票退订界面')

		# 日期
		self.date = '2021-6-28'
		self.lb1 = QLabel(self)
		self.lb1.setGeometry(20,20,210,30)
		self.lb1.setText(self.date)
		self.lb1.setAlignment(Qt.AlignCenter)

		# 身份证号
		self.lb2 = QLabel(self)
		self.lb2.setGeometry(20,65,70,30)
		self.lb2.setText('身份证：')
		self.lb2.setAlignment(Qt.AlignLeft)

		self.le1 = QLineEdit(self)
		self.le1.setGeometry(105,60,150,30)

		# 订单号
		self.lb3 = QLabel(self)
		self.lb3.setGeometry(20,105,70,30)
		self.lb3.setText('订单号：')
		self.lb3.setAlignment(Qt.AlignLeft)

		self.le2 = QLineEdit(self)
		self.le2.setGeometry(105,100,150,30)

		# 查询状态
		self.lb4 = QLabel(self)
		self.lb4.setGeometry(20,145,210,30)
		self.lb4.setText('查询状态： 无')
		self.lb4.setAlignment(Qt.AlignLeft)

		# 退订状态
		self.lb5 = QLabel(self)
		self.lb5.setGeometry(20,185,210,30)
		self.lb5.setText('退订状态： 无')
		self.lb5.setAlignment(Qt.AlignLeft)

		# 查询
		self.pb1 = QPushButton('查询',self)
		self.pb1.setGeometry(20,265,100,30)
		self.pb1.clicked.connect(self.query)

		# 退订
		self.pb2 = QPushButton('退订',self)
		self.pb2.setGeometry(20,225,230,30)
		self.pb2.setEnabled(False)
		self.pb2.clicked.connect(self.unsubscribe)

		# 返回
		self.pb3 = QPushButton('返回',self)
		self.pb3.setGeometry(150,265,100,30)
		self.pb3.clicked.connect(self.back)

		self.show()

	def unsubscribe(self):
		'''
		退订
		'''
		self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')
		cursor = self.airinfo.cursor()

		sql = 'SELECT InfoId, status FROM OrderInfo WHERE InfoID = ' + self.le2.text() + \
			' AND IDNumber = "' + self.le1.text() + '";'
		cursor.execute(sql)
		data = cursor.fetchall()

		if data:
			if data[0][1] == 0: # 如果已经取票或者已经退票均不能再退票
				try:
					sql = 'DELETE FROM GetTicketInfo WHERE InfoID = ' + self.le2.text() + ';'
					cursor.execute(sql)
					self.airinfo.commit()

					sql = 'DELETE FROM BillInfo WHERE InfoID = ' + self.le2.text() + ';'
					cursor.execute(sql)
					self.airinfo.commit()

					sql = 'UPDATE OrderInfo SET status = 2 WHERE InfoID = ' + self.le2.text() + ';'
					cursor.execute(sql)
					self.airinfo.commit()
				except:
					self.airinfo.rollback()

				cursor.close()
				self.airinfo.close()

				QMessageBox.information(self,'提示','机票退订成功！')
				self.lb5.setText('退订状态： 成功')
				self.pb2.setEnabled(False)

			elif data[0][1] == 1:
				QMessageBox.information(self,'提示','机票已取，退订失败！')	
				self.lb5.setText('退订状态： 失败')
				self.pb2.setEnabled(False)

				cursor.close()
				self.airinfo.close()

			elif data[0][1] == 2:
				QMessageBox.information(self,'提示','机票已退，退订失败！')	
				self.lb5.setText('退订状态： 失败')
				self.pb2.setEnabled(False)

				cursor.close()
				self.airinfo.close()

		else:
			QMessageBox.information(self,'提示','输入订单号或身份证号有误！')	
			self.lb5.setText('退订状态： 失败')
			self.pb2.setEnabled(False)

			cursor.close()
			self.airinfo.close()

	def query(self):
		'''
		查询取票通知
		'''
		self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')
		cursor = self.airinfo.cursor()

		try:
			sql = 'SELECT InfoID FROM OrderInfo WHERE IDNumber = "' +\
				self.le1.text() + '" AND InfoID = ' + self.le2.text() + ';'
			cursor.execute(sql)

			data = cursor.fetchall()
			cursor.close()
			self.airinfo.close()

			if data:
				self.lb4.setText('查询状态： 成功')
				self.lb5.setText('退订状态： 无')
				self.pb2.setEnabled(True)
			else:
				self.lb4.setText('查询状态： 失败')
				self.lb5.setText('退订状态： 无')
				self.pb2.setEnabled(False)
		except:
			self.lb4.setText('查询状态： 失败')
			self.lb5.setText('退订状态： 无')
			self.pb2.setEnabled(False)

	def back(self):
		'''
		返回
		'''
		self.hide()
		self.us = user_select.select_window()
		self.us.show()