-- 创建 airinfo 数据库
CREATE DATABASE IF NOT EXISTS airinfo;

USE airinfo;

SET foreign_key_checks = 0;

DROP TABLE IF EXISTS DirectInfo;
DROP TABLE IF EXISTS TransitInfo;
DROP TABLE IF EXISTS SeatInfo;
DROP TABLE IF EXISTS OrderInfo;
DROP TABLE IF EXISTS GetTicketInfo;
DROP TABLE IF EXISTS BillInfo;

-- 直达信息表
CREATE TABLE DirectInfo(
	airlineName CHAR(30), -- 航空公司名
	flightNumber CHAR(8), -- 航班号
	craftTypeName CHAR(30), -- 机型
	airdate DATE NOT NULL, -- 时间
	departureCity CHAR(30) NOT NULL, -- 出发城市
	departureAirport CHAR(50) NOT NULL, -- 出发机场
	departureTime CHAR(10) NOT NULL, -- 出发时间
	arrivalCity CHAR(30) NOT NULL, -- 到达城市
	arrivalAirport CHAR(50) NOT NULL, -- 到达机场
	arrivalTime CHAR(15) NOT NULL, -- 到达时间
	stopoverCity CHAR(30), -- 经停城市
	lowestPrice CHAR(5) NOT NULL, -- 最低票价
	punctualRate CHAR(10), -- 准时率
	PRIMARY KEY(airdate, flightNumber, departureCity, arrivalCity)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
	
-- 中转信息表
CREATE TABLE TransitInfo(
	airdate DATE NOT NULL, -- 时间
	airlineName CHAR(60), -- 航空公司名
	flightNumber CHAR(20), -- 航班号
	departureCity CHAR(30) NOT NULL, -- 出发城市
	departureAirport CHAR(50) NOT NULL, -- 出发机场
	departureTime CHAR(10) NOT NULL, -- 出发时间
	arrivalCity CHAR(30) NOT NULL, -- 到达城市
	arrivalAirport CHAR(50) NOT NULL, -- 到达机场
	arrivalTime CHAR(15) NOT NULL, -- 到达时间
	transitCity CHAR(30), -- 中转城市
	transitInterval CHAR(25), -- 中转间隔
	lowestPrice CHAR(5) NOT NULL, -- 最低票价
	punctualRate CHAR(20), -- 准时率
	PRIMARY KEY(airdate, flightNumber, departureCity, arrivalCity)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 航班座位信息表
CREATE TABLE SeatInfo(
	airdate DATE NOT NULL, -- 时间
	flightNumber CHAR(15) NOT NULL, -- 航班号
	departureCity CHAR(30) NOT NULL, -- 出发城市
	arrivalCity CHAR(30) NOT NULL, -- 到达城市
	seats VARCHAR(320) NOT NULL, -- 座位
	PRIMARY KEY(airdate, flightNumber, departureCity, arrivalCity)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 旅客订票信息表
CREATE TABLE OrderInfo(
	InfoID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, -- 记录号
	lastname CHAR(20) NOT NULL, -- 姓
	firstname CHAR(20) NOT NULL, -- 名
	IDnumber CHAR(18) NOT NULL, -- 身份证号
	DorT SMALLINT CHECK (DorT IN (0,1)), -- 直达或中转
	airdate DATE NOT NULL, -- 时间
	flightNumber CHAR(20), -- 航班号
	departureCity CHAR(30) NOT NULL, -- 出发城市
	arrivalCity CHAR(30) NOT NULL, -- 到达城市
	seat CHAR(8) NOT NULL, -- 座位
	status SMALLINT CHECK (status IN (0,1,2)) -- 状态
)ENGINE=InnoDB DEFAULT CHARSET=utf8;	

-- 取票通知表
CREATE TABLE GetTicketInfo(
	InfoID INT NOT NULL PRIMARY KEY, -- 记录号
	token CHAR(8) NOT NULL, -- 取票号
	PickDate DATE NOT NULL, -- 取票时间
	FOREIGN KEY (InfoID) REFERENCES OrderInfo(InfoID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;	

-- 账单
CREATE TABLE BillInfo(
	InfoID INT NOT NULL PRIMARY KEY, -- 记录号
	price CHAR(5) NOT NULL, -- 票价
	PayMethod SMALLINT CHECK(PayMethod IN (0,1)), -- 支付方式
	PayDate DATE NOT NULL, -- 支付日期
	FOREIGN KEY (InfoID) REFERENCES OrderInfo(InfoID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;	