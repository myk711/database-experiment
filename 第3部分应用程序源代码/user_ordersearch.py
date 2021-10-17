from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import user_select # 用户选择界面
import sys, pymysql, datetime

class user_ordersearch(QWidget):
	'''
	订单查询页面
	'''
	def __init__(self):
		super().__init__()
		self.initUI()
		self.connectdb()

	def initUI(self):
		'''
		初始化界面
		'''
		self.setFont(QFont("Arial",12))
		#self.setGeometry(300,300,800,500)
		self.setFixedSize(self.width(),self.height())
		self.setWindowTitle('订单查询页面')

		self.vbox = QVBoxLayout()
		# 身份证号
		self.hbox1 = QHBoxLayout()
		self.lb1 = QLabel(self)
		#self.lb1.setGeometry(50,30,100,30)
		self.lb1.setText('身份证号：')
		self.lb1.setAlignment(Qt.AlignLeft)

		self.le1 = QLineEdit(self)
		#self.le1.setGeometry(150,20,200,30)
		self.hbox1.addWidget(self.lb1)
		self.hbox1.addWidget(self.le1)

		# 查询状态
		self.lb2 = QLabel(self)
		#self.lb2.setGeometry(50,70,300,30)
		self.lb2.setText('查询状态： 无')
		self.lb2.setAlignment(Qt.AlignLeft)

		# 数据库连接状态
		self.lb3 = QLabel(self)
		#self.lb3.setGeometry(420,25,200,30)
		self.lb3.setText('数据库连接状态： 未连接')

		self.hbox2 = QHBoxLayout()

		# 查询
		self.pb1 = QPushButton('查询',self)
		#self.pb1.setGeometry(450,65,100,30)
		self.pb1.clicked.connect(self.query)

		# 返回
		self.pb2 = QPushButton('返回',self)
		#self.pb2.setGeometry(600,65,100,30)
		self.pb2.clicked.connect(self.back)

		self.hbox2.addWidget(self.pb1)
		self.hbox2.addWidget(self.pb2)

		# 连接数据库
		self.pb3 = QPushButton('连接数据库',self)
		#self.pb3.setGeometry(650,25,100,30)
		self.pb3.clicked.connect(self.connectdb)

		# 表
		self.tb = QTableWidget(self)
		#self.tb.setGeometry(20,120,760,360)

		self.vbox.addLayout(self.hbox1)
		self.vbox.addWidget(self.lb2)
		self.vbox.addLayout(self.hbox2)
		self.vbox.addWidget(self.lb3)
		self.vbox.addWidget(self.pb3)
		self.vbox.addWidget(self.tb)

		self.setLayout(self.vbox)


	def connectdb(self):
		'''
		连接数据库
		'''
		try:
			self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')
			self.lb3.setText('数据库连接状态： 已连接')
			self.pb3.setEnabled(False)
		except:
			pass

	def query(self):
		'''
		查询
		'''
		if not self.pb3.isEnabled():
			cursor = self.airinfo.cursor()

			sql = 'SELECT InfoID, DorT, airdate, flightNumber, departureCity, \
				arrivalCity, seat, status FROM OrderInfo WHERE IDNumber = "' + self.le1.text() + '";'
			cursor.execute(sql)
			data = cursor.fetchall()

			self.lb2.setText('查询记录： 查询到记录%d条' % len(data))

			self.tb.setRowCount(len(data))
			self.tb.setColumnCount(8)
			self.tb.setHorizontalHeaderLabels(['账单号','直达或中转','日期','航班号','出发城市','到达城市','座位','状态'])
			self.tb.setEditTriggers(QAbstractItemView.NoEditTriggers)

			# 数据插入 部分数据要转换一下形式便于显示
			for i in range(len(data)):
				for j in range(8):
					if j == 1:
						newItem = QTableWidgetItem('直达' if data[i][1]==0 else '中转')
						self.tb.setItem(i,j,newItem)
					elif j == 6:
						d = data[i][j].split()
						dic = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F'}
						#转化格式
						if len(d) == 1:
							row = str(int((int(d[0])+1)/6 + 1))#行
							col = dic[int(d[0]) % 6]#列
							item = row + col
						elif len(d) == 2:
							row = []
							col = []
							#首列
							row.append(str(int(int(d[0])/6) + 1))
							col.append(dic[int(d[0]) % 6])

							#尾列
							row.append(str(int((int(d[1]))/6) + 1))
							col.append(dic[int(d[1]) % 6])
							item = row[0] + col[0] + ' ' + row[1] + col[1]
						newItem = QTableWidgetItem(item) # 座位从1开始
						self.tb.setItem(i,j,newItem)
					elif j == 7:
						if data[i][j] == 0:
							s = '未取票'
						elif data[i][j] == 1:
							s = '已取票'
						else:
							s = '已退票'
						newItem = QTableWidgetItem(s)
						self.tb.setItem(i,j,newItem)
					else:
						newItem = QTableWidgetItem(str(data[i][j]))
						self.tb.setItem(i,j,newItem)

			cursor.close()		

			# 大于等于1条视为查询成功
			if len(data) > 0:
				QMessageBox.information(self,'提示','查询成功！')

		else:
			QMessageBox.information(self,'提示','请先连接数据库！')

	
	def back(self):
		'''
		返回
		'''
		self.hide()
		self.sw = user_select.select_window()
		self.sw.show()