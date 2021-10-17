from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from limits import * # 属性限制信息
import user_select # 用户选择界面
import sys, pymysql, re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
 # 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)

class user_airstatus(QDialog):
	'''
	航班预定状况
	'''
	def __init__(self):
		super().__init__()
		self.tl = time_limit[1:]
		self.cs = ['北京'] + citys 
		self.initUI()

	def initUI(self):
		'''
		初始化界面
		'''
		self.setFont(QFont("Arial",12))
		self.resize(400,600)
		self.setFixedSize(self.width(),self.height())
		self.setWindowTitle('航班预订状况')

		# 日期
		self.lb1 = QLabel(self)
		self.lb1.setText('出发日期：')
		self.lb1.setAlignment(Qt.AlignLeft)

		self.pb3 = QPushButton('修改',self)
		self.pb3.clicked.connect(self.change_query)

		# 航班号
		self.lb2 = QLabel(self)
		self.lb2.setText('　航班号：')
		self.lb2.setAlignment(Qt.AlignLeft)

		self.pb4 = QPushButton('修改',self)
		self.pb4.clicked.connect(self.change_query)

		# 出发城市
		self.lb3 = QLabel(self)
		self.lb3.setText('出发城市：')
		self.lb3.setAlignment(Qt.AlignLeft)

		self.pb5 = QPushButton('修改',self)
		self.pb5.clicked.connect(self.change_query)

		# 到达城市
		self.lb4 = QLabel(self)
		self.lb4.setText('到达城市：')
		self.lb4.setAlignment(Qt.AlignLeft)

		self.pb6 = QPushButton('修改',self)
		self.pb6.clicked.connect(self.change_query)

		# 查询
		self.pb1 = QPushButton('查询',self)
		self.pb1.clicked.connect(self.query)

		# 返回
		self.pb2 = QPushButton('返回',self)
		self.pb2.clicked.connect(self.back)

		# 航班满座率
		self.lb5 = QLabel(self)
		self.lb5.setText('航班满座率： 无')
		self.lb5.setAlignment(Qt.AlignLeft)

		# 作图区		
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)

		# 布局
		hbox1 = QHBoxLayout()
		hbox1.addWidget(self.lb1)
		hbox1.addStretch(3)
		hbox1.addWidget(self.pb3)

		hbox2 = QHBoxLayout()
		hbox2.addWidget(self.lb2)
		hbox2.addStretch(3)
		hbox2.addWidget(self.pb4)

		hbox3 = QHBoxLayout()
		hbox3.addWidget(self.lb3)
		hbox3.addStretch(3)
		hbox3.addWidget(self.pb5)

		hbox4 = QHBoxLayout()
		hbox4.addWidget(self.lb4)
		hbox4.addStretch(3)
		hbox4.addWidget(self.pb6)

		hbox5 = QHBoxLayout()
		hbox5.addWidget(self.pb1)
		hbox5.addWidget(self.pb2)

		vbox = QVBoxLayout()
		vbox.addLayout(hbox1)
		vbox.addLayout(hbox2)
		vbox.addLayout(hbox3)
		vbox.addLayout(hbox4)
		vbox.addLayout(hbox5)
		vbox.addWidget(self.lb5)
		vbox.addWidget(self.canvas)

		self.setLayout(vbox)

	def change_query(self):
		'''
		修改查询信息
		'''
		s = self.sender()

		if s == self.pb3:
			text, ok = QInputDialog.getItem(self, '修改', '请输入出发时间：',self.tl)
			if text not in self.tl:
				QMessageBox.warning(self,'警告','输入不符合要求！',QMessageBox.Yes,QMessageBox.Yes)
			elif ok:
				self.lb1.setText('出发日期： ' + text) 

		elif s == self.pb4:
			text, ok = QInputDialog.getText(self, '修改', '请输入航班号：')
			match = re.compile(r'^\w{2}\d{4}\s\w{2}\d{4}$|^\w{2}\d{4}$').match(text)
			if not match:
				QMessageBox.warning(self,'警告','输入不符合要求！',QMessageBox.Yes,QMessageBox.Yes)
			elif ok:
				self.lb2.setText('　航班号： ' + text) 

		elif s == self.pb5:
			text, ok = QInputDialog.getItem(self, '修改', '请输入出发城市：',self.cs)
			if text not in self.cs:
				QMessageBox.warning(self,'警告','输入不符合要求！',QMessageBox.Yes,QMessageBox.Yes)
			elif ok:
				self.lb3.setText('出发城市： ' + text)

		elif s == self.pb6:
			text, ok = QInputDialog.getItem(self, '修改', '请输入到达城市：',self.cs)
			if text not in self.cs:
				QMessageBox.warning(self,'警告','输入不符合要求！',QMessageBox.Yes,QMessageBox.Yes)
			elif ok:
				self.lb4.setText('到达城市： ' + text) 


	def query(self):
		'''
		查询并作图
		'''

		if self.lb1.text()[6:]=='' or self.lb2.text()[6:]=='' or self.lb3.text()[6:]=='' \
			or self.lb4.text()[6:]=='':
			QMessageBox.information(self,'提示','请确认信息完整再查询！')
		else:
			self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')

			cursor = self.airinfo.cursor()

			sql = 'SELECT concat("\t",SeatInfo.seats) FROM SeatInfo WHERE airdate = "%s" AND flightNumber = "%s" AND \
				departureCity = "%s" AND arrivalCity = "%s";' % (self.lb1.text()[6:],self.lb2.text()[6:],
					self.lb3.text()[6:],self.lb4.text()[6:])

			cursor.execute(sql)
			data = cursor.fetchall()
			if data:
				data = data[0][0]

				count_1 = data.count('1')
				count_0 = len(data) - count_1
				x = [count_1, count_0]
				labels = ['Sold', 'Not Sold']

				plt.clf() # 清除上一个figure

				plt.pie(x = x, labels=labels,autopct='%.1f%%')
				plt.title('Sold Rate')

				self.canvas.draw()
				self.lb5.setText('航班满座率： %.3f%%' % (100.0*count_1/len(data)))
			else:
				QMessageBox.information(self,'提示','无效航班！')
				self.lb5.setText('航班满座率： 无')
				plt.clf()

			cursor.close()
			self.airinfo.close()

	def back(self):
		'''
		返回
		'''
		self.hide()
		self.sw = user_select.select_window()
		self.sw.show()

