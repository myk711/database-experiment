from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from limits import * # 属性限制信息
import login # 登录界面
import user_select # 用户选择界面
import sys, pymysql, re, random, time, datetime

class InputInfo(QWidget):
	'''
	订票时输入有关信息
	'''
	def __init__(self,allinfo,tag,seat):
		super().__init__()
		self.allinfo = allinfo # 购票信息
		self.tag = tag # 直达或中转
		self.date = '2021-06-28'
		self.seat = seat
		self.initUI()

	def initUI(self):
		'''
		初始化界面
		'''
		self.setFont(QFont("Arial",12))
		self.resize(370,360)
		self.setFixedSize(self.width(),self.height())
		self.setWindowTitle('订票基本信息输入')

		self.hbox1 = QHBoxLayout()
		# 姓
		self.lb1 = QLabel(self)
		#self.lb1.setGeometry(20,20,30,30)
		self.lb1.setText('姓：')
		self.lb1.setAlignment(Qt.AlignLeft)
		self.hbox1.addWidget(self.lb1)

		self.le1 = QLineEdit(self)
		#self.le1.setGeometry(60,15,100,30)
		self.hbox1.addWidget(self.le1)

		# 名
		self.lb2 = QLabel(self)
		#self.lb2.setGeometry(200,20,30,30)
		self.lb2.setText('名：')
		self.lb2.setAlignment(Qt.AlignLeft)
		self.hbox1.addWidget(self.lb2)

		self.le2 = QLineEdit(self)
		#self.le2.setGeometry(240,15,110,30)
		self.hbox1.addWidget(self.le2)

		self.hbox2 = QHBoxLayout()
		# 身份证号码
		self.lb3 = QLabel(self)
		#self.lb3.setGeometry(20,65,80,30)
		self.lb3.setText('身份证号：')
		self.lb3.setAlignment(Qt.AlignLeft)

		self.le3 = QLineEdit(self)
		#self.le3.setGeometry(110,60,240,30)
		self.hbox2.addWidget(self.lb3)
		self.hbox2.addWidget(self.le3)

		self.hbox3 = QHBoxLayout()
		# 支付方式
		self.lb4 = QLabel(self)
		#self.lb4.setGeometry(20,105,80,30)
		self.lb4.setText('支付方式：')
		self.lb4.setAlignment(Qt.AlignLeft)

		self.rb1 = QRadioButton('微信',self)
		#self.rb1.setGeometry(130,100,80,30)
		self.rb1.setChecked(True)

		self.rb2 = QRadioButton('支付宝',self)
		#self.rb2.setGeometry(230,100,80,30)

		self.hbox3.addWidget(self.lb4)
		self.hbox3.addWidget(self.rb1)
		self.hbox3.addWidget(self.rb2)

		# 提示信息
		self.lb5 = QLabel(self)
		#self.lb5.setGeometry(20,145,350,120)

		# 直达
		if self.tag == 0:
			showtext = '尊敬的用户，\n您将订购' + \
				self.allinfo[0] + '\n' +  self.allinfo[1] + self.allinfo[2] +\
				'航班，\n' + self.allinfo[4] + self.allinfo[5] + ' ' + self.allinfo[6] +\
				'出发，\n' + self.allinfo[7] + self.allinfo[8] + ' ' + self.allinfo[9] +\
				'到达，\n'
			if self.allinfo[10]:
				showtext += '经停' + self.allinfo[10] +'，'
			showtext += '票价' + self.allinfo[11] + '元'

			self.lb5.setText(showtext)

		# 中转
		elif self.tag == 1:
			showtext = '尊敬的用户，\n您将订购' + self.allinfo[0] + '\n' 
			if self.allinfo[1] and self.allinfo[2]:
				s1 = self.allinfo[1].split()
				s2 = self.allinfo[2].split()
				showtext += s1[0] + s2[0] + '和' + s1[1] + s2[1] + '航班，\n'
			else:
				showtext += '某航班，\n'
			showtext += self.allinfo[3] + self.allinfo[4] + ' ' + self.allinfo[5] +\
				'出发，\n' + self.allinfo[6] + self.allinfo[7] + ' ' + self.allinfo[8] +\
				'到达，\n'
			if self.allinfo[9] and self.allinfo[10]:
				showtext += '中转' + self.allinfo[9] + self.allinfo[10] +'，\n'
			else:
				showtext += '某地中转，\n'
			showtext += '票价' + self.allinfo[11] + '元'

			self.lb5.setText(showtext)

		# 确定
		self.pb1 = QPushButton('确定',self)
		self.pb1.setGeometry(20,275,330,30)
		self.pb1.clicked.connect(self.infosure)
		
		# 打印取票通知
		self.pb2 = QPushButton('打印取票通知和账单',self)
		self.pb2.setGeometry(20,315,330,30)
		self.pb2.setEnabled(False)
		self.pb2.clicked.connect(self.print_get_ticket_and_bill)

		self.vbox = QVBoxLayout()
		self.vbox.addLayout(self.hbox1)
		self.vbox.addLayout(self.hbox2)
		self.vbox.addLayout(self.hbox3)
		self.vbox.addWidget(self.lb5)
		self.vbox.addWidget(self.pb1)
		self.vbox.addWidget(self.pb2)

		self.setLayout(self.vbox)

		self.show()

	def check(self):
		'''
		检查输入信息的完整性
		'''
		if not (self.le1.text() and self.le2.text()): # 姓名不可缺失
			return False
		else:
			m = re.compile(r'^\d{18}$').match(self.le3.text()) # 且身份证号长度必须为18位
			if m:
				return True
			else:
				return False

	def infosure(self):
		'''
		输入信息确认
		'''
		reply = QMessageBox.information(self, '提示','您确定信息无误吗？',QMessageBox.No | QMessageBox.Yes,QMessageBox.Yes)
		if reply == QMessageBox.Yes:
			if self.check():
				QMessageBox.information(self,'提示','恭喜您！订票成功！',QMessageBox.Ok)
				self.pb1.setEnabled(False)
				self.pb2.setEnabled(True)
				token = self.generatetoken() # 生成取票密码
				InfoID = self.insert_order() # 插入新的旅客订票信息
				self.all_get_ticket_info = self.insert_get_ticket(InfoID, token) # 插入新的取票通知信息
				self.all_bill_info = self.insert_bill(InfoID) # 插入新的账单信息
				self.take_seat() # 将座位标记为0
			else:
				QMessageBox.information(self,'提示','姓名信息缺失或身份证号长度有误，请检查！',QMessageBox.Ok)
	
	def take_seat(self):
		'''
		占座
		'''
		self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')
		cursor = self.airinfo.cursor()

		# 直达
		if self.tag == 0:
			sql = 'SELECT seats FROM SeatInfo WHERE airdate = "%s" AND flightNumber = "%s" AND departureCity = "%s" \
				AND arrivalCity = "%s";' % (self.allinfo[0], self.allinfo[2], self.allinfo[4], self.allinfo[7])
			cursor.execute(sql)
			s = cursor.fetchall()[0][0]
			l = list(s)
			l[self.seat[0]] = '0'
			s = ''.join(l)

			sql = 'UPDATE SeatInfo SET seats = "%s" WHERE airdate = "%s" AND flightNumber = "%s" AND departureCity = "%s" \
				AND arrivalCity = "%s";' % (s, self.allinfo[0], self.allinfo[2], self.allinfo[4], self.allinfo[7])

		# 中转
		elif self.tag == 1:
			sql = 'SELECT seats FROM SeatInfo WHERE airdate = "%s" AND flightNumber = "%s" AND departureCity = "%s" \
				AND arrivalCity = "%s";' % (self.allinfo[0], self.allinfo[2], self.allinfo[3], self.allinfo[6])
			cursor.execute(sql)
			s = cursor.fetchall()[0][0]
			l = list(s)
			l[self.seat[0]] = '0'
			l[self.seat[1]] = '0'
			s = ''.join(l)

			sql = 'UPDATE SeatInfo SET seats = "%s" WHERE airdate = "%s" AND flightNumber = "%s" AND departureCity = "%s" \
				AND arrivalCity = "%s";' % (s, self.allinfo[0], self.allinfo[2], self.allinfo[3], self.allinfo[6])

		try:
			cursor.execute(sql)
			self.airinfo.commit()
		except:
			self.airinfo.rollback()

		cursor.close()
		self.airinfo.close()

	def insert_order(self):
		'''
		插入旅客订票信息
		'''
		self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')
		cursor = self.airinfo.cursor()

		# 直达
		if self.tag == 0:
			sql = 'INSERT INTO OrderInfo VALUES (DEFAULT,"%s","%s",%d,%d,"%s","%s","%s","%s","%s",%d);' % \
				(self.le1.text(), self.le2.text(), int(self.le3.text()), self.tag, self.allinfo[0], self.allinfo[2],\
				self.allinfo[4], self.allinfo[7], str(self.seat[0]), 0) # 0 表示未取票

		elif self.tag == 1:
			sql = 'INSERT INTO OrderInfo VALUES (DEFAULT,"%s","%s",%d,%d,"%s","%s","%s","%s","%s",%d);' % \
				(self.le1.text(), self.le2.text(), int(self.le3.text()), self.tag, self.allinfo[0], self.allinfo[2],\
				self.allinfo[3], self.allinfo[6], str(self.seat[0])+' '+str(self.seat[1]), 0) # 0 表示未取票

		try:
			cursor.execute(sql)
			self.airinfo.commit()
		except:
			self.airinfo.rollback()

		sql = 'SELECT MAX(InfoID) FROM OrderInfo;'
		cursor.execute(sql)
		data = cursor.fetchall()

		cursor.close()
		self.airinfo.close()

		return data[0][0] #返回当前InfoID

	def insert_get_ticket(self,infoid,token):
		'''
		插入取票通知
		'''
		self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')
		cursor = self.airinfo.cursor()

		# 计算取票时间(-1)
		d = datetime.datetime.strptime(self.allinfo[0],'%Y-%m-%d')
		d = d - datetime.timedelta(days=1)
		d = d.strftime("%Y-%m-%d") 

		sql = 'INSERT INTO GetTicketInfo VALUES (%d,"%s","%s");' % \
			(infoid, token, d)
		try:
			cursor.execute(sql)
			self.airinfo.commit()
		except:
			self.airinfo.rollback()

		cursor.close()
		self.airinfo.close()

		data = [infoid,token,d]

		return data

	def insert_bill(self,id):
		'''
		插入账单
		'''
		self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')
		cursor = self.airinfo.cursor()

		if self.rb1.isChecked():
			method = 0
		else:
			method = 1

		sql = 'INSERT INTO BillInfo VALUES (%d,%d,%d,"%s");' % \
			(id, int(self.allinfo[11]), method, self.date)

		try:
			cursor.execute(sql)
			self.airinfo.commit()
		except:
			self.airinfo.rollback()

		cursor.close()
		self.airinfo.close()

		data = [id,int(self.allinfo[11]),method,self.date]

		return data

	def generatetoken(self):
		'''
		生成六位随机取票密码
		'''
		while 1:
			token = ''
			for i in range(6):
				num = random.randint(0, 9)
				letter = chr(random.randint(97, 122)) #取小写字母
				Letter = chr(random.randint(65, 90)) #取大写字母
				s = str(random.choice([num,letter,Letter]))
				token += s

			# 检查是否有重复密码
			self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')
			cursor = self.airinfo.cursor()

			sql = 'SELECT token FROM GetTicketInfo WHERE token = "%s";' % token
			cursor.execute(sql)
			data = cursor.fetchall()
			if not data: 
				return token
			else:
				pass

	def print_get_ticket_and_bill(self):
		'''
		打印取票通知和账单
		'''
		self.hide()
		self.pgtab = GetTicket_Bill(self.all_get_ticket_info, self.all_bill_info)
		self.pgtab.show()

class GetTicket_Bill(QMainWindow):
	'''
	取票通知单
	'''
	def __init__(self,info1,info2):
		super().__init__()
		self.info1 = info1
		self.info2 = info2
		self.initUI()

	def initUI(self):
		'''
		初始化界面
		'''
		self.setFont(QFont("Arial",14))
		self.resize(620,400)
		self.setFixedSize(self.width(),self.height())
		self.setWindowTitle('取票通知单和账单')

		text1 = '机场取票通知单' + '\n\n' +\
			   '账单号:    ' + str(self.info1[0]) + '\n' +\
			   '取票密码:  ' + self.info1[1] + '\n' +\
			   '取票时间:  ' + self.info1[2] + '\n'

		# 左侧为取票通知单
		self.lb1 = QLabel(self)
		self.lb1.setGeometry(0,0,300,300)
		self.lb1.setText(text1)
		self.lb1.setAlignment(Qt.AlignCenter)

		if self.info2[2] == 0:
			method = '微信'
		else:
			method = '支付宝'

		text2 = '账单' + '\n\n' +\
			   '账单号:    ' + str(self.info2[0]) + '\n' +\
			   '金额:     ' + str(self.info2[1]) + '\n' +\
			   '支付方式:  ' + method + '\n' +\
			   '支付日期:  ' + self.info2[3] + '\n'

		# 右侧为取票通知单
		self.lb2 = QLabel(self)
		self.lb2.setGeometry(320,0,300,300)
		self.lb2.setText(text2)
		self.lb2.setAlignment(Qt.AlignCenter)

		self.pb1 = QPushButton('返回',self)
		self.pb1.setGeometry(90,320,120,50)
		self.pb1.clicked.connect(self.back)

		self.pb2 = QPushButton('打印',self)
		self.pb2.setGeometry(390,320,120,50)
		self.pb2.clicked.connect(self.Print)

	def Print(self):
		'''
		打印
		'''
		screen = QApplication.primaryScreen()
		pix1 = screen.grabWindow(self.lb1.winId())
		pix1.save('取票通知单'+str(self.info1[0])+'.jpg')

		screen = QApplication.primaryScreen()
		pix2 = screen.grabWindow(self.lb2.winId())
		pix2.save('账单'+str(self.info2[0])+'.jpg')

		QMessageBox.information(self,'提示','打印成功！',QMessageBox.Ok)

	def back(self):
		'''
		返回
		'''
		self.hide()
		self.airsearch = AirSearch()
		self.airsearch.show()

class AirSearch(QMainWindow):
	'''
	航班查询界面
	'''
	def __init__(self):
		super().__init__()
		self.initUI()
		self.connectdb() #自动连接

	def initUI(self):
		'''
		初始化界面
		'''

		#更改尺寸
		self.setFont(QFont("Arial",12))
		self.resize(1180,580)
		self.setFixedSize(self.width(),self.height())
		self.setWindowTitle('机票预订系统')


		# 出港或入港
		self.rb1 = QRadioButton('出港',self)
		self.rb1.setGeometry(25,30,100,50)
		self.rb1.setChecked(True)
		self.rb1.pressed.connect(self.valid_port)

		self.rb2 = QRadioButton('入港',self)
		self.rb2.setGeometry(150,30,100,50)
		self.rb2.pressed.connect(self.valid_port)

		# 修改查询要求
		self.lb1 = QLabel(self)
		self.lb1.setGeometry(20,105,175,50)
		self.lb1.setText('出发城市： 北京')
		self.lb1.setAlignment(Qt.AlignLeft)

		self.pb1 = QPushButton('修改',self)
		self.pb1.setGeometry(200,100,50,30)
		self.pb1.setEnabled(False)
		self.pb1.clicked.connect(self.change_query)

		self.lb2 = QLabel(self)
		self.lb2.setGeometry(20,180,175,50)
		self.lb2.setText('到达城市： 阿尔山')
		self.lb2.setAlignment(Qt.AlignLeft)

		self.pb2 = QPushButton('修改',self)
		self.pb2.setGeometry(200,175,50,30)
		self.pb2.clicked.connect(self.change_query)

		self.lb3 = QLabel(self)
		self.lb3.setGeometry(20,255,175,50)
		self.lb3.setText('出发日期： 不限')
		self.lb3.setAlignment(Qt.AlignLeft)

		self.pb3 = QPushButton('修改',self)
		self.pb3.setGeometry(200,250,50,30)
		self.pb3.clicked.connect(self.change_query)

		self.lb4 = QLabel(self)
		self.lb4.setGeometry(20,330,175,50)
		self.lb4.setText('票价上限： 不限')
		self.lb4.setAlignment(Qt.AlignLeft)

		self.pb4 = QPushButton('修改',self)
		self.pb4.setGeometry(200,325,50,30)
		self.pb4.clicked.connect(self.change_query)

		self.lb5 = QLabel(self)
		self.lb5.setGeometry(20,405,175,50)
		self.lb5.setText('是否经停： 不限')
		self.lb5.setAlignment(Qt.AlignLeft)

		self.pb5 = QPushButton('修改',self)
		self.pb5.setGeometry(200,400,50,30)
		self.pb5.clicked.connect(self.change_query)

		self.lb6 = QLabel(self)
		self.lb6.setGeometry(20,480,175,50)
		self.lb6.setText('所属航司： 不限')
		self.lb6.setAlignment(Qt.AlignLeft)

		self.pb6 = QPushButton('修改',self)
		self.pb6.setGeometry(200,475,50,30)
		self.pb6.clicked.connect(self.change_query)

		self.pb7 = QPushButton('连接',self)
		self.pb7.setGeometry(10,530,80,30)
		self.pb7.clicked.connect(self.connectdb)

		self.pb8 = QPushButton('查询',self)
		self.pb8.setGeometry(100,530,80,30)
		self.pb8.clicked.connect(self.query)

		self.pb9 = QPushButton('返回',self)
		self.pb9.setGeometry(190,530,80,30)
		self.pb9.clicked.connect(self.back)

		# 选项卡网格
		self.tb = QTabWidget(self)
		self.tb.setGeometry(275,5,900,570)

		# 直达表格支持右键菜单
		self.tb1 = QTableWidget() 
		self.tb1.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tb1.customContextMenuRequested.connect(self.GenerateMenuDirect)

		# 中转表格支持右键菜单
		self.tb2 = QTableWidget() 
		self.tb2.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tb2.customContextMenuRequested.connect(self.GenerateMenuTransit)

		self.tb.addTab(self.tb1,"直达")
		self.tb.addTab(self.tb2,"中转")

		self.show()

	def valid_port(self):
		'''
		出港航班和入港航班选定后要限制按钮修改
		'''
		s = self.sender()

		if s == self.rb1:
			self.lb1.setText('出发城市： 北京')
			self.pb1.setEnabled(False)
			self.lb2.setText('到达城市： 阿尔山')
			self.pb2.setEnabled(True)

		elif s == self.rb2:
			self.lb1.setText('出发城市： 阿尔山')
			self.pb1.setEnabled(True)
			self.lb2.setText('到达城市： 北京')
			self.pb2.setEnabled(False)

	def change_query(self):
		'''
		修改查询信息
		'''
		s = self.sender()

		if s == self.pb1:
			text, ok = QInputDialog.getItem(self, '修改', '请输入出发城市：',citys)
			if text not in citys:
				QMessageBox.warning(self,'警告','输入不符合要求！',QMessageBox.Yes,QMessageBox.Yes)
			elif ok:
				self.lb1.setText('出发城市： ' + text)

		elif s == self.pb2:
			text, ok = QInputDialog.getItem(self, '修改', '请输入到达城市：',citys)
			if text not in citys:
				QMessageBox.warning(self,'警告','输入不符合要求！',QMessageBox.Yes,QMessageBox.Yes)
			elif ok:
				self.lb2.setText('到达城市： ' + text) 

		elif s == self.pb3:
			text, ok = QInputDialog.getItem(self, '修改', '请输入出发时间：',time_limit)
			if text not in time_limit:
				QMessageBox.warning(self,'警告','输入不符合要求！',QMessageBox.Yes,QMessageBox.Yes)
			elif ok:
				self.lb3.setText('出发日期： ' + text) 

		elif s == self.pb4:
			text, ok = QInputDialog.getItem(self, '修改', '请输入票价上限：',price_limit)
			if text not in price_limit:
				QMessageBox.warning(self,'警告','输入不符合要求！',QMessageBox.Yes,QMessageBox.Yes)
			elif ok:
				self.lb4.setText('票价上限： ' + text)

		elif s == self.pb5:
			op = ['不限','是','否']
			text, ok = QInputDialog.getItem(self, '修改', '请输入是否中转：',op)
			if text not in op:
				QMessageBox.warning(self,'警告','输入不符合要求！',QMessageBox.Yes,QMessageBox.Yes)			
			elif ok:
				self.lb5.setText('是否中转： ' + text) 

		elif s == self.pb6:
			text, ok = QInputDialog.getItem(self, '修改', '请输入所属航司：',airline_limit)
			if text not in airline_limit:
				QMessageBox.warning(self,'警告','输入不符合要求！',QMessageBox.Yes,QMessageBox.Yes)		
			elif ok:
				self.lb6.setText('所属航司： ' + text) 

	def connectdb(self):
		'''
		连接数据库
		'''
		try:
			self.airinfo = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666666',database='airinfo',charset='utf8')
			self.pb7.setText('已连接')
			self.pb7.setEnabled(False)
		except:
			pass

	def query(self):
		'''
		查询
		'''
		if not self.pb7.isEnabled():

			# 先查直达表
			cursor = self.airinfo.cursor()

			sql = 'SELECT * FROM DirectInfo WHERE departureCity = "' + self.lb1.text()[6:]\
				+ '" AND arrivalCity = "' + self.lb2.text()[6:] + '"'

			# 对非不限的项添加到sql语句中
			if self.lb3.text()[6:] != '不限':
				sql += ' AND airdate = "' + self.lb3.text()[6:] + '"'
			if self.lb4.text()[6:] != '不限':
				sql += ' AND lowestPrice <= ' + self.lb4.text()[6:]
			if self.lb5.text()[6:] == '是': #是否经停仅对直达表有效
				sql += ' AND stopoverCity IS NOT NULL' 
			elif self.lb5.text()[6:] == '否':
				sql += ' AND stopoverCity IS NULL'
			if self.lb6.text()[6:] != '不限':
				sql += ' AND airlineName = "' + self.lb6.text()[6:] + '"'
			sql += ';'

			cursor.execute(sql)
			data = cursor.fetchall()

			self.tb1.setRowCount(len(data))
			self.tb1.setColumnCount(13)
			self.tb1.setHorizontalHeaderLabels(['日期','航空公司','航班号','飞机型号','出发城市','出发机场','出发时间'\
					,'到达城市','到达机场','到达时间','经停','票价','预估准时率'])
			# self.tw.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # 横向自适应伸缩模式
			self.tb1.setEditTriggers(QAbstractItemView.NoEditTriggers) # 不允许用户编辑

			for i in range(len(data)):
				for j in range(13):
					newItem = QTableWidgetItem(str(data[i][j]))
					self.tb1.setItem(i,j,newItem)
			cursor.close()

			# 再查中转表
			cursor = self.airinfo.cursor()

			sql = 'SELECT * FROM TransitInfo WHERE departureCity = "' + self.lb1.text()[6:]\
				+ '" AND arrivalCity = "' + self.lb2.text()[6:] + '"'

			# 对非不限的项添加到sql语句中
			if self.lb3.text()[6:] != '不限':
				sql += ' AND airdate = "' + self.lb3.text()[6:] + '"'
			if self.lb4.text()[6:] != '不限':
				sql += ' AND lowestPrice <= ' + self.lb4.text()[6:]
			if self.lb6.text()[6:] != '不限':
				sql += ' AND (airlineName LIKE "' + self.lb6.text()[6:] + '%" OR airlineName LIKE "%' +\
					self.lb6.text()[6:] + '")'
			sql += ';'

			cursor.execute(sql)
			data = cursor.fetchall()

			self.tb2.setRowCount(len(data))
			self.tb2.setColumnCount(13)
			self.tb2.setHorizontalHeaderLabels(['日期','航空公司','航班号','出发城市','出发机场','出发时间'\
					,'到达城市','到达机场','到达时间','中转城市','中转时间','票价','预估准时率'])
			# self.tw.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # 横向自适应伸缩模式
			self.tb2.setEditTriggers(QAbstractItemView.NoEditTriggers) # 不允许用户编辑

			for i in range(len(data)):
				for j in range(13):
					newItem = QTableWidgetItem(str(data[i][j]))
					self.tb2.setItem(i,j,newItem)
			cursor.close()
		else:
			QMessageBox.warning(self,'警告','请先连接数据库！',QMessageBox.Yes,QMessageBox.Yes)	

	def GetSeat(self,info,tag):
		'''
		获取座位
		'''
		cursor = self.airinfo.cursor()

		# 直达
		if tag == 0:
			sql = 'SELECT seats FROM SeatInfo WHERE airdate = "%s" AND flightNumber = "%s" AND \
				departureCity = "%s" AND arrivalCity = "%s";' % (info[0],info[2],info[4],info[7])
		# 中转
		elif tag == 1:
			sql = 'SELECT seats FROM SeatInfo WHERE airdate = "%s" AND flightNumber = "%s" AND \
				departureCity = "%s" AND arrivalCity = "%s";' % (info[0],info[2],info[3],info[6])

		cursor.execute(sql)
		data = cursor.fetchall()

		if data:
			data = data[0][0]
		else:
			return [-1,-1]

		# 直达
		if tag == 0:
			data = re.compile(r'\d+').search(data).group(0)
			index = data.find('1',int(len(data)/4))
			return [index, index]

		# 中转
		elif tag == 1:
			data = re.compile(r'\d+').search(data).group(0)
			index1 = data.find('1',int(len(data)/4))
			index2 = data.find('1',int(len(data)/4*3))#瞎选的
			return [index1, index2]

	def GenerateMenuDirect(self,pos):
		'''
		直达页面菜单
		'''
		row = self.tb1.rowCount()
		row_num = -1

		# 获取当前行数，从0开始
		for i in self.tb1.selectionModel().selection().indexes():
			row_num = i.row()

		if row_num < row:
			menu = QMenu()
			order = menu.addAction(u'订票')
			action = menu.exec_(self.tb1.mapToGlobal(pos))
			if action == order:
				allinfo = []
				for i in range(13):
					info = self.tb1.item(row_num,i).text()
					allinfo.append(info)

				reply = QMessageBox.information(self, '提示','您确定要订票吗？',QMessageBox.No | QMessageBox.Yes,QMessageBox.Yes)
				if reply == QMessageBox.Yes:
					seat = self.GetSeat(allinfo,0) # 获取座位
					if seat[0] > -1:
						self.hide()
						self.input = InputInfo(allinfo,0,seat)
						self.input.show()
					else:
						QMessageBox.information(self, '提示','航班已售罄！',QMessageBox.Ok)

	def GenerateMenuTransit(self,pos):
		'''
		中转页面菜单
		'''
		row = self.tb2.rowCount()
		row_num = -1

		# 获取当前行数，从0开始
		for i in self.tb2.selectionModel().selection().indexes():
			row_num = i.row()

		if row_num < row:
			menu = QMenu()
			order = menu.addAction(u'订票')
			action = menu.exec_(self.tb2.mapToGlobal(pos))
			if action == order:
				allinfo = []
				for i in range(13):
					info = self.tb2.item(row_num,i).text()
					allinfo.append(info)

				reply = QMessageBox.information(self, '提示','您确定要订票吗？',QMessageBox.No | QMessageBox.Yes,QMessageBox.Yes)
				if reply == QMessageBox.Yes:
					seat = self.GetSeat(allinfo,1) # 获取座位
					if seat[0] > -1:
						self.hide()
						self.input = InputInfo(allinfo,1,seat)
						self.input.show()
					else:
						QMessageBox.information(self, '提示','航班已售罄！',QMessageBox.Ok)

	def back(self):
		'''
		返回到选择页面
		'''
		self.hide()
		self.us = user_select.select_window()
		self.us.show()

	def logout(self):
		'''
		注销
		'''
		self.hide()
		self.login = login.login()
		self.login.show()

	def about_sys(self):
		'''
		关于系统
		'''
		QMessageBox.about(self,'关于系统','机票预订系统\n版本：Version 1.0')

	def about_author(self):
		'''
		关于作者
		'''
		QMessageBox.about(self,'关于作者','作者: 王辰潇\n学校: 华中科技大学\n班级：校交1803\n学号：U201816136')
