from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from login import * # 登录界面

# 登录
if __name__ == '__main__':
	app = QApplication(sys.argv)
	dialog = login()
	dialog.show()
	sys.exit(app.exec_())
