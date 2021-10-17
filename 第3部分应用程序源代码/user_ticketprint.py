from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import user_select # 用户选择界面
import sys, pymysql, datetime

class ticketprint(QWidget):
	'''
	打印机票页面
	'''
	def __init__(self,info,tag):
		super().__init__()
		self.info = info[0]
		self.tag = tag # 0为直达 1为中转
		self.initUI()
		
	def initUI(self):
		'''
		初始化界面
		'''
		self.setFont(QFont("Arial",14))
		self.resize(1200,250)
		self.setFixedSize(self.width(),self.height())
		self.setWindowTitle('机票')


		# 机票信息预处理

		# 直达
		if self.tag == 0:
			i7 = self.info[8] # 机型
			if i7 == '':
				i7 = '未知'
			i14 = self.info[15] # 经停
			if i14 == '':
				i14 = '无'

			dic = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F'}

			row = str(int((int(self.info[4])+1)/6 + 1))
			col = dic[int(self.info[4]) % 6]

			# 机票信息
			text1 = '姓： %s\n名： %s\n身份证号码： %s\n日期： %s\n' % (self.info[1],self.info[2],self.info[3],self.info[5].strftime("%Y-%m-%d")) 
			text2 = '航空公司： %s\n航班号： %s\n机型： %s\n经停： %s\n' % (self.info[6],self.info[7],i7,i14)
			text3 = '出发机场： %s\n到达机场： %s\n预计出发时间： %s\n预计到达时间： %s\n' % (self.info[9]+self.info[10],self.info[12]+self.info[13],self.info[11],self.info[14])
			text4 = '票价： %s元' % (self.info[16])
			text6 = '座位： %s%s\n' % (row,col)

		# 中转
		elif self.tag == 1:
			# 航司组合 航班号组合
			s1 = self.info[6].split()
			s2 = self.info[7].split()

			# 座位变换
			dic = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F'}
			sit = self.info[4].split() 

			row = []
			col = []

			#首列
			row.append(str(int(int(sit[0])/6) + 1))
			col.append(dic[int(sit[0]) % 6])

			#尾列
			row.append(str(int((int(sit[1])-150)/6) + 1))
			col.append(dic[int(sit[1]) % 6])

			# 机票信息
			text1 = '姓： %s\n名： %s\n身份证： %s\n日期： %s\n' % (self.info[1],self.info[2],self.info[3],self.info[5].strftime("%Y-%m-%d"))
			text2 = '首段航司： %s\n首段航班号： %s\n末段航司： %s\n末段航班号： %s\n' % (s1[0],s2[0],s1[1],s2[1])
			text3 = '出发机场： %s\n到达机场： %s\n预计出发时间： %s\n预计到达时间： %s\n' % (self.info[8]+self.info[9],self.info[11]+self.info[12],self.info[10],self.info[13])
			text4 = '票价： %s元' % (self.info[16])
			text6 = '座位： %s%s->%s%s\n' % (row[0],col[0],row[1],col[1])

		self.vbox=QVBoxLayout()
		self.hbox = QHBoxLayout()
		# 第一列
		self.c1 = QLabel(self)
		#self.c1.setGeometry(20,150,320,110)
		self.c1.setText(text1)
		self.c1.setAlignment(Qt.AlignLeft)
		self.hbox.addWidget(self.c1)
		# 第二列
		self.c2 = QLabel(self)
		#self.c2.setGeometry(340,150,320,110)
		self.c2.setText(text2)
		self.c2.setAlignment(Qt.AlignLeft)
		self.hbox.addWidget(self.c2)
		# 第三列
		self.c3 = QLabel(self)
		#self.c3.setGeometry(680,150,300,110)
		self.c3.setText(text3)
		self.c3.setAlignment(Qt.AlignLeft)
		self.hbox.addWidget(self.c3)

		self.vbox.addLayout(self.hbox)


		self.hbox2 = QHBoxLayout()
		# 末行左 票价
		self.c4 = QLabel(self)
		#self.c4.setGeometry(20,270,300,30)
		self.c4.setText(text4)
		self.c4.setAlignment(Qt.AlignLeft)
		self.hbox2.addWidget(self.c4)

		# 末行右 座位
		self.c6 = QLabel(self)
		#self.c6.setGeometry(680,270,300,30)
		self.c6.setText(text6)
		self.c6.setAlignment(Qt.AlignLeft)
		self.hbox2.addWidget(self.c6)

		self.vbox.addLayout(self.hbox2)
		# 中转信息
		if self.tag == 1:
			text5 = '中转： ' + self.info[14] + self.info[15]
			self.c5 = QLabel(self)
			#self.c5.setGeometry(340,270,300,30)
			self.c5.setText(text5)
			self.c5.setAlignment(Qt.AlignLeft)
			self.vbox.addWidget(self.c5)

		self.hbox3 = QHBoxLayout()
		# 打印
		self.pb1 = QPushButton('打印',self)
		self.pb1.resize(100,50)
		self.pb1.clicked.connect(self.Print)

		# 返回
		self.pb2 = QPushButton('返回',self)
		self.pb2.resize(100,50)
		self.pb2.clicked.connect(self.back)
		self.hbox3.addWidget(self.pb1)
		self.hbox3.addWidget(self.pb2)
		self.vbox.addLayout(self.hbox3)
		self.setLayout(self.vbox)
		self.show()

	def Print(self):
		'''
		打印
		'''
		screen = QApplication.primaryScreen()
		pix = screen.grabWindow(self.winId(),0,0,1200,250)
		pix.save('机票'+str(self.info[0])+'.jpg')

		# 修改状态为已取票，且删除取票通知单
		InfoID = self.info[0]

		self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')
		cursor = self.airinfo.cursor()

		try:
			sql = 'DELETE FROM GetTicketInfo WHERE InfoID = ' + str(InfoID) + ';'
			cursor.execute(sql)
			self.airinfo.commit()

			sql = 'UPDATE OrderInfo SET status = 1 WHERE InfoID = ' + str(InfoID) + ';'
			cursor.execute(sql)
			self.airinfo.commit()
		except:
			self.airinfo.rollback()

		cursor.close()
		self.airinfo.close()

		self.pb1.setEnabled(False) # 不允许重复打印

		QMessageBox.information(self,'提示','打印成功！',QMessageBox.Ok)

	def back(self):
		'''
		返回
		'''
		self.hide()
		self.sw = user_select.select_window()
		self.sw.show()

class user_ticketprint(QDialog):
	'''
	打印机票页面
	'''
	def __init__(self):
		super().__init__()
		self.date = '2021-6-28'
		self.InfoID = -1
		self.initUI()
		
	def initUI(self):
		'''
		初始化界面
		'''
		self.setFont(QFont("Arial",12))
		#self.setGeometry(300,300,250,275)
		self.resize(300, 300)
		self.setWindowTitle('机票打印界面')
		self.setFixedSize(self.width(), self.height())

		# 账单号
		self.lb1 = QLabel(self)
		#self.lb2.setGeometry(20,65,80,30)
		self.lb1.setText('账单编号：')
		self.lb1.setAlignment(Qt.AlignLeft)

		self.le1 = QLineEdit(self)
		#self.le1.setGeometry(110,60,100,30)

		self.hbox1 = QHBoxLayout()
		self.hbox1.addWidget(self.lb1)
		self.hbox1.addWidget(self.le1)

		# 取票密码
		self.lb2 = QLabel(self)
		#self.lb2.setGeometry(20,105,80,30)
		self.lb2.setText('取票密码：')
		self.lb2.setAlignment(Qt.AlignLeft)

		self.le2 = QLineEdit(self)
		#self.le2.setGeometry(110,100,100,30)

		self.hbox2 = QHBoxLayout()
		self.hbox2.addWidget(self.lb2)
		self.hbox2.addWidget(self.le2)
		self.hbox3 = QHBoxLayout()

		# 查询状态
		self.lb3 = QLabel(self)
		#self.lb3.setGeometry(20,145,210,30)
		self.lb3.setText('查询状态： 无')
		self.lb3.setAlignment(Qt.AlignLeft)
		self.hbox3.addWidget(self.lb3)
		# 确定
		self.pb1 = QPushButton('确定',self)
		#self.pb1.setGeometry(20,185,210,30)
		self.pb1.clicked.connect(self.query)

		# 预览并打印
		self.pb2 = QPushButton('预览并打印',self)
		#self.pb2.setGeometry(20,225,100,30)
		self.pb2.setEnabled(False)
		self.pb2.clicked.connect(self.check_and_print)

		# 返回
		self.pb3 = QPushButton('返回',self)
		#self.pb3.setGeometry(130,225,100,30)
		self.pb3.clicked.connect(self.back)

		self.vbox = QVBoxLayout()
		self.vbox.addLayout(self.hbox1)
		self.vbox.addLayout(self.hbox2)
		self.vbox.addLayout(self.hbox3)
		self.vbox.addWidget(self.pb1)
		self.vbox.addWidget(self.pb2)
		self.vbox.addWidget(self.pb3)
		self.setLayout(self.vbox)

	def check_and_print(self):
		'''
		预览并打印
		'''
		self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')
		cursor = self.airinfo.cursor()

		sql = 'SELECT * FROM OrderInfo WHERE InfoID = ' + str(self.InfoID) + ';'
		cursor.execute(sql)

		data = cursor.fetchall()
		if data[0][9] == 1:
			QMessageBox.information(self,'提示','机票已经被打印，打印失败！')
		elif data[0][9] == 2:
			QMessageBox.information(self,'提示','机票已经被退订，打印失败！')
		else:
			# 直达
			if data[0][4] == 0:
				d = data[0][5].strftime('%Y-%m-%d') # 将datetime变为string
				sql = 'SELECT InfoID, lastname, firstname, IDNumber, seat, DirectInfo.* FROM DirectInfo, OrderInfo ' +\
					'WHERE DirectInfo.airdate = "' + d + '" AND DirectInfo.flightNumber = "' + \
					data[0][6] + '" AND DirectInfo.departureCity = "' + data[0][7] + '" AND DirectInfo.arrivalCity = "' + \
					data[0][8] + '"' + ' AND DirectInfo.airdate = OrderInfo.airdate AND DirectInfo.flightNumber = OrderInfo.flightNumber ' +\
					'AND DirectInfo.departureCity = OrderInfo.departureCity AND DirectInfo.arrivalCity = OrderInfo.arrivalCity;'
				cursor.execute(sql)
				data_direct = cursor.fetchall()
				#print(data_direct)

				# 打开直达机票打印界面
				self.hide()
				self.dtp = ticketprint(data_direct, 0)
				self.dtp.show()

			# 中
			elif data[0][4] == 1:
				d = data[0][5].strftime('%Y-%m-%d') # 将datetime变为string
				sql = 'SELECT InfoID, lastname, firstname, IDNumber, seat, TransitInfo.* FROM TransitInfo, OrderInfo ' +\
					'WHERE TransitInfo.airdate = "' + d + '" AND TransitInfo.flightNumber = "' +\
					data[0][6] + '" AND TransitInfo.departureCity = "' + data[0][7] + '" AND TransitInfo.arrivalCity = "' +\
					data[0][8] + '"' + ' AND TransitInfo.airdate = OrderInfo.airdate AND TransitInfo.flightNumber = OrderInfo.flightNumber ' +\
					'AND TransitInfo.departureCity = OrderInfo.departureCity AND TransitInfo.arrivalCity = OrderInfo.arrivalCity;'
				#print(sql)
				cursor.execute(sql)
				data_transit = cursor.fetchall()
				# print(data_transit)

				# 打开中转机票打印界面
				self.hide()
				self.ttp = ticketprint(data_transit, 1)
				self.ttp.show()

		cursor.close()
		self.airinfo.close()

	def query(self):
		'''
		查询取票通知
		'''
		self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')
		cursor = self.airinfo.cursor()

		sql = 'SELECT InfoID FROM GetTicketInfo WHERE InfoID = "' + self.le1.text() + '" AND token = "' +\
			self.le2.text() + '";'

		cursor.execute(sql)
		data = cursor.fetchall()
		cursor.close()
		self.airinfo.close()

		if data:
			self.lb3.setText('查询状态： 成功')
			self.pb2.setEnabled(True)
			self.InfoID = data[0][0]
		else:
			self.lb3.setText('查询状态： 失败')
			self.InfoID = -1

	def back(self):
		'''
		返回
		'''
		self.hide()
		self.sw = user_select.select_window()
		self.sw.show()

