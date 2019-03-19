import urllib.request
import re
import ssl
import urllib.parse
import http.cookiejar
import datetime
import time
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#为了防止ssl出现问题
ssl._create_default_https_context = ssl._create_unverified_context
context = ssl._create_unverified_context()

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'}

#设置超时时间
socket.setdefaulttimeout(60)

def getszm():	
	with open('szm.txt','r') as f:
		szmtext=f.read() 
	pat = 'var station_names =\'(.*?)\';'
	szmstr = re.compile(pat).findall(szmtext)[0]
	szmarr = szmstr.split('@')[1:]
	szm = {}
	for i in szmarr:
		info = i.split('|')
		# print(info)	
		szm[info[1]] = info[2]
	return szm

szm = getszm()

yzmdict = {
	'1':'33,43',	 
	'2':'103,46',	  
	'3':'168,45',	   
	'4':'247,49',		 
	'5':'36,122',		 
	'6':'105,118',	  
	'7':'185,122',	
	'8':'247,118'	 
}

setsDetailInfo = {
	#0.车次
	'车次':0, 
	#1.start
	'start':1,
	#2.to
	'to':2,
	#3.出发时间
	'begin':3,
	#4.到达时间
	'end':4,
	#5.历时
	'alltime':5,
	#6.高级软卧
	'高软':6,
	#7.软卧
	'软卧':7,
	#8.软座
	'软座':8,
	#9.无座
	'无座':9,
	#10.硬卧
	'硬卧':10,
	#11.硬座
	'硬座':11,
	#12.二等座
	'二等':12,
	#13.一等座
	'一等':13,
	#14.商务座
	'商务':14,
	#15.动卧
	'动卧':15,
	#16.train_no
	'train_no':16,
	#17.leftTicket
	'leftTicket':17,
	#18.train_location
	'train_location':18,
	#19.订票码
	'train_location':19
}

trainSets = {
	'商务':'9',
	'一等':'M',
	'二等':'O',
	'硬卧':'3',
	'硬座':'1',
	'软卧':'4',
	'高软':'6',
	'无座':'1',
	'动卧':'F'
}


#反转三字码字典
def reDict():

	d = szm
	nwdic = {v:k for k,v in d.items()}
	return nwdic

rd = reDict()
#查票
INDEX = 0
def checkTic(date,start,to,student):
	global INDEX
	TIC = ['','A','B','X','O','C','D','E','F','J','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','W','Y','Z']
	
	while True:
		try:
			#查票接口url
			ticketUrl = 'https://kyfw.12306.cn/otn/leftTicket/query%s?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=%s'%(TIC[INDEX],date,start,to,student)
			print(ticketUrl)

			req = urllib.request.Request(url = ticketUrl,headers = header)	 
			res = urllib.request.urlopen(req)	 
			data = res.read().decode("utf-8","ignore")
			patrst01='"result":\["(.*?)\]'
			rst01=re.compile(patrst01).findall(data)[0]
			allcheci=rst01.split(",")

			#checimap_pat='"map":({.*?})'
			#checimap=eval(re.compile(checimap_pat).findall(data)[0])

			infolist = []
			for item in allcheci:
				infolist.append(item.split('|'))
			trains = []
			for item in infolist: 
				train = []			
				#0.车次
				# print(item)  
				train.append(item[3])
				#始发站
				# train.append(rd[item[2]])
				#终点站
				# train.append(rd[item[3]])
				#1.from
				train.append(rd[item[6]])
				#2.to
				train.append(rd[item[7]])
				#3.出发时间
				train.append(item[8])
				#4.到达时间
				train.append(item[9])
				#5.历时
				train.append(item[10])
				#6.高级软卧
				train.append(item[21])
				#7.软卧
				train.append(item[23])
				#8.软座
				train.append(item[24])
				#9.无座
				train.append(item[26])
				#10.硬卧
				train.append(item[28])
				#11.硬座
				train.append(item[29])
				#12.二等座
				train.append(item[30])
				#13.一等座
				train.append(item[31])
				#14.商务座
				train.append(item[32])
				#15.动卧
				train.append(item[34])
				#16.train_no
				train.append(item[2])
				#17.leftTicket
				train.append(item[12])
				#18.train_location
				train.append(item[15])
				#19.订票码
				train.append(item[0])
				trains.append(train)
			return trains
		except Exception:
			print('更新查票链接中。。。')
			INDEX = INDEX+1
			print(INDEX)
			if INDEX==len(TIC):
				INDEX = 0
#展示车票
def showTic(trains):
	for item in trains:
		for i in range(16):
			if item[i] == '':
				item[i] = '/'
		# print(item[0]+'\t '+item[1]+'\t '+item[2]+'\t '+item[3]+'\t '+item[4]+'\t '+item[5]+'\t '+item[6]+'\t '+item[7]+'\t '+item[8]+'\t '+item[9]+'\t '+item[10]+'\t '+item[11]+'\t '+item[12]+'\t '+item[13]+'\t '+item[14]+'\t '+item[15]+'\t ')
		# print(item[0]+'\t '+item[1]+'\t '+item[2]+'\t '+item[3]+'\t '+item[4]+'\t '+item[5]+'\t '+item[6]+'\t '+item[7]+'\t '+item[8]+'\t '+item[9]+'\t '+item[10]+'\t '+item[11]+'\t '+item[12]+'\t '+item[13]+'\t '+item[14]+'\t '+item[15])
		# print('(车次)'+item[0]+'\t(起点)'+item[1]+'\t(终点)'+item[2]+'\t(发时)'+item[3]+'\t(到时)'+item[4]+'\t(历时)'+item[5]+'\t(高软)'+item[6]+'\t(软卧)'+item[7]+'\t(软座)'+item[8]+'\t(无座)'+item[9]+'\t(硬卧)'+item[10]+'\t(硬座)'+item[11]+'\t(二等)'+item[12]+'\t(一等)'+item[13]+'\t(商务)'+item[14]+'\t(动卧)'+item[15])
		print('(车次)'+item[0]+'\t(起点)'+item[1]+'\t(终点)'+item[2]+'\t(发时)'+item[3]+'\t(到时)'+item[4]+'\t(历时)'+item[5]+'\t(高软)'+item[6]+'\t(软卧)'+item[7]+'\t(软座)'+item[8]+'\t(无座)'+item[9]+'\t(硬卧)'+item[10]+'\t(硬座)'+item[11]+'\t(二等)'+item[12]+'\t(一等)'+item[13]+'\t(商务)'+item[14])
		print()
	
def makePassOld(pasInfo,checkIndex,sets,stuyn):
	#构造passengerTicketStr
	if stuyn == 'y':
		fastP = '%s,0,3,%s,1,%s,,N'
		anoP  = '_%s,0,3,%s,1,%s,,N'
	else :
		fastP = '%s,0,1,%s,1,%s,,N'
		anoP  = '_%s,0,1,%s,1,%s,,N'

	# 构造oldPassengerStr
	olds = '%s,1,%s,%s_'
	
	if len(checkIndex) == 1:
		# print('%s,0,1,1,,N'%trainSets[sets])
		passengerTicketStr = fastP %(trainSets[sets],pasInfo[checkIndex[0]][0],pasInfo[checkIndex[0]][1])
		# print(passengerTicketStr)
		if pasInfo[checkIndex[0]][2] == '学生':
			if stuyn == 'n':
				oldPassengerStr = olds %(pasInfo[checkIndex[0]][0],pasInfo[checkIndex[0]][1],'3')
			if stuyn == 'y':
				oldPassengerStr = olds %(pasInfo[checkIndex[0]][0],pasInfo[checkIndex[0]][1],'3')
		elif pasInfo[checkIndex[0]][2] == '成人':
			oldPassengerStr = olds % (pasInfo[checkIndex[0]][0], pasInfo[checkIndex[0]][1],'1')
			
		else:
			oldPassengerStr = ''
			print('submitTick oldPassengerStr构造错误1')
	elif len(checkIndex) >1:
		passengerTicketStr = ''
		oldPassengerStr =''
		for i in checkIndex:
			passengerTicketStr = passengerTicketStr+anoP %(trainSets[sets],pasInfo[i][0],pasInfo[i][1])
			oldPa = ''
			if pasInfo[i][2] == '学生':
				oldPa = olds % (pasInfo[i][0], pasInfo[i][1], '3')
			elif pasInfo[i][2] == '成人':
				oldPa = olds % (pasInfo[i][0], pasInfo[i][1], '1')
			else:
				oldPa = ''
				print('submitTick oldPassengerStr构造错误2')
			oldPassengerStr = oldPassengerStr+oldPa	 
		passengerTicketStr = passengerTicketStr[1:]
	return [passengerTicketStr,oldPassengerStr] 
	
#发送邮件
def send(rec):
	sender = 'flaskgagaga@foxmail.com'
	receivers = rec
	message =  MIMEMultipart('related')
	subject = 'yzm'
	message['Subject'] = subject
	message['From'] = sender
	message['To'] = receivers
	content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>','html','utf-8')
	message.attach(content)

	file=open("yzm.jpg", "rb")
	img_data = file.read()
	file.close()

	img = MIMEImage(img_data)
	img.add_header('Content-ID', 'imageid')
	message.attach(img)

	try:
		server=smtplib.SMTP_SSL("smtp.qq.com",465)
		server.login(sender,"dielqfliatmqbcdj")
		server.sendmail(sender,receivers,message.as_string())
		server.quit()
		print ("邮件发送成功")
	except smtplib.SMTPException as e:
		print(e)

#发送邮件2
def sends(rec):
	sender = 'flaskgagaga@foxmail.com'
	receivers = rec
	message =  MIMEMultipart('related')
	subject = '12306抢票成功'
	message['Subject'] = subject
	message['From'] = sender
	message['To'] = receivers
	content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>','html','utf-8')
	message.attach(content)

	file=open("succeed.jpg", "rb")
	img_data = file.read()
	file.close()

	img = MIMEImage(img_data)
	img.add_header('Content-ID', 'imageid')
	message.attach(img)

	try:
		server=smtplib.SMTP_SSL("smtp.qq.com",465)
		server.login(sender,"dielqfliatmqbcdj")
		server.sendmail(sender,receivers,message.as_string())
		server.quit()
		print ("邮件发送成功")
	except smtplib.SMTPException as e:
		print(e)

		
