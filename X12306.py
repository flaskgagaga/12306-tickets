from head import *

# szm={"北京":"BJP","南京":"NJH"}
szm = getszm()

#反转三字码字典
rd = reDict()
		
##一、查票

#infomation
#start1="北京"
start1=input("请输入起始站：")
start=szm[start1]

#to1="上海"
to1=input("请输入到站：")
to=szm[to1]

#isstudent="0"
isstudent=input("是学生吗？(y/n)：")

#date="2018-10-20"
date=input("请输入要查询的乘车开始日期的年月，如2018-10-10：")

if isstudent=="n":
	student="ADULT"
elif isstudent=="y":
	student="0X00"
else:
	print('没有这个选项，默认不是学生')
	student="ADULT"


#查票，并展示
trains = checkTic(date,start,to,student)
showTic(trains)

isdo=input("查票完成，请输入1继续…：")
#是否继续
if(isdo==1 or isdo=="1"):
	pass
else:
	raise Exception("输入不是1，结束执行：")
	
print("Cookie处理中…")
#以下进行登陆操作
#建立cookie处理
cjar=http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
urllib.request.install_opener(opener)

#循环登陆
while True:
	try:		
		##二、以下进入自动登录部分
		loginurl="https://kyfw.12306.cn/otn/login/init#"
		req0 = urllib.request.Request(url=loginurl,headers=header)
		req0data=urllib.request.urlopen(req0).read().decode("utf-8","ignore")

		#验证码URL 得到图片
		yzmurl="https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand"

		while True:
			urllib.request.urlretrieve(yzmurl,'yzm.jpg')
			rec=input("请输入邮箱号接受验证码：")
			send(rec)
			yzmIndex=input("请输入验证码，输入第几张图片即可：")
			if(yzmIndex!="re"):
				break				   
		yzmIndexList = yzmIndex.split(' ')
		yzmResuit=''
		for i in yzmIndexList:
			yzmResuit = yzmResuit+yzmdict[i]+','
		yzmResuit = yzmResuit[0:-1] 
		print(yzmResuit)

		#post验证码验证
		yzmposturl="https://kyfw.12306.cn/passport/captcha/captcha-check"
		yzmpostdata =urllib.parse.urlencode({
		"answer":yzmResuit,
		"rand":"sjrand",
		"login_site":"E",
		}).encode('utf-8')
		req1 = urllib.request.Request(url = yzmposturl,data = yzmpostdata,headers = header)
		req1data=urllib.request.urlopen(req1).read().decode("utf-8","ignore")

		#post账号密码验证
		username = input('请输入12306账号：')
		pwd = input('请输入密码：')

		loginposturl="https://kyfw.12306.cn/passport/web/login"
		loginpostdata =urllib.parse.urlencode({
		"username":username,
		"password":pwd,
		"appid":"otn",
		}).encode('utf-8')
		req2 = urllib.request.Request(url=loginposturl,data=loginpostdata,headers=header)
		req2data=urllib.request.urlopen(req2).read().decode("utf-8","ignore")

		#其他验证
		#验证1
		loginposturl2="https://kyfw.12306.cn/otn/login/userLogin"
		loginpostdata2 =urllib.parse.urlencode({
		"_json_att":"",
		}).encode('utf-8')
		req2_2 = urllib.request.Request(url=loginposturl2,data=loginpostdata2,headers=header)
		req2data_2=urllib.request.urlopen(req2_2).read().decode("utf-8","ignore")

		#验证2
		loginposturl3="https://kyfw.12306.cn/passport/web/auth/uamtk"
		loginpostdata3 =urllib.parse.urlencode({
		"appid":"otn",
		}).encode('utf-8')
		#获取tk，下一个请求需要tk
		req2_3 = urllib.request.Request(url=loginposturl3,data=loginpostdata3,headers=header)
		req2data_3=urllib.request.urlopen(req2_3).read().decode("utf-8","ignore")
		pat_req2='"newapptk":"(.*?)"'
		tk=re.compile(pat_req2,re.S).findall(req2data_3)[0]

		
		#验证3post tk
		loginposturl4="https://kyfw.12306.cn/otn/uamauthclient"
		loginpostdata4 =urllib.parse.urlencode({
		"tk":tk,
		}).encode('utf-8')
		req2_4 = urllib.request.Request(loginposturl4,loginpostdata4)
		req2_4.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
		req2data_4=urllib.request.urlopen(req2_4).read().decode("utf-8","ignore")
	except Exception:
		print('\n**************验证码或账号密码错误！请重新输入***************\n')
	else:
		break

#爬个人中心页面
centerurl="https://kyfw.12306.cn/otn/index/initMy12306"
req3 = urllib.request.Request(url=centerurl,headers=header)
req3data=urllib.request.urlopen(req3).read().decode("utf-8","ignore")
print("\n&&&&&登陆成功&&&&&\n")

#isdo="1"
isdo=input("如果需要订票，请输入1继续，否则请输入其他数据：")
if(isdo==1 or isdo=="1"):
	pass
else:
	raise Exception("输入不是1，结束执行")
thiscode=input("请输入要预定的车次：")
thisseats=input('请输入坐席：')

##爬取乘客
checkPas = None

#自动post网址4-获取乘客信息
userurl = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'

userurlreq = urllib.request.Request(url = userurl,headers=header)
userurlreqdata = urllib.request.urlopen(userurlreq).read().decode('utf8')

pat = '"passenger_name":"(.*?)".*?"passenger_id_no":"(.*?)".*?"passenger_type_name":"(.*?)"'
passengerInfo = re.compile(pat,re.S).findall(userurlreqdata)
# print(passengerInfo)
for i in passengerInfo:
	print(i)

#选择乘客
checkPas = input('请选择乘客：')
checkPas = checkPas.split(' ')
checkIndex = [int(i)-1 for i in checkPas]


##三、订票
pas_old = None
count = 0
while True:
	###四、时间检查
	curtime = time.time()
	lotime = time.localtime(curtime)
	if lotime[3] < 6 or (lotime[3] > 23 or (lotime[3] == 23 and lotime[4] > 0)):
		print('当前时间：%s-%s-%s %s-%s-%s'%(lotime[0],lotime[1],lotime[2],lotime[3],lotime[4],lotime[5]))
		time.sleep(1)
		continue
	else:		
		try:
			#先初始化一下订票界面
			initurl="https://kyfw.12306.cn/otn/leftTicket/init"
			reqinit=urllib.request.Request(url=initurl,headers=header)
			initdata=urllib.request.urlopen(reqinit).read().decode("utf-8","ignore")
			
			#再爬对应订票信息
			trains=checkTic(date,start,to,student)
			
			#code 是所有车次号  secretStr 是所有订票码
			code=[]
			secretStr=[]
			for i in trains:
				code.append(i[0])
				secretStr.append(i[19])
				if i[0] == thiscode:
					train = i
			
			#用字典trainzy存储车次有没有票的信息
			# trainzy={}
			# for i in range(0,len(code)):
				# trainzy[code[i]]=zy[i]
				
			#用字典traindata存储车次secretStr信息，以供后续订票操作
			#存储的格式是：traindata={"车次1":secretStr1,"车次2":secretStr2,…} 
			traindata={}
			for i in range(0,len(code)):
				traindata[code[i]]=secretStr[i]
				
			#订票-第1次post-主要进行确认用户状态
			checkurl="https://kyfw.12306.cn/otn/login/checkUser"
			checkdata =urllib.parse.urlencode({
			"_json_att":""
			}).encode('utf-8')
			req5 = urllib.request.Request(url=checkurl,data=checkdata,headers=header)
			req5data=urllib.request.urlopen(req5).read().decode("utf-8","ignore")
			
			#自动得到当前时间并转为年-月-格式，因为后面请求数据需要用到当前时间作为返程时间backdate
			backdate=datetime.datetime.now()
			backdate=backdate.strftime("%Y-%m-%d")
			secretStr=train[19].replace('%2F','/').replace('%2B','+').replace('%0A','').replace('%3D','=').replace('"','')
			
			# 构造 seatType,purpose_codes,学生和成人不一样，后面会用到
			if isstudent == 'y':
				seatType = '1'
				purpose_codes = '0X00'
			else :
				seatType = '3'
				purpose_codes = '00'
			
			#订票-第2次post-主要进行“预订”提交	
			submiturl="https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
			submitdata =urllib.parse.urlencode({
			"secretStr":secretStr,
			"train_date":date,
			"back_train_date":backdate,
			"tour_flag":"dc",
			"purpose_codes":purpose_codes,
			"query_from_station_name":start1,
			"query_to_station_name":to1,
			'undefined':''
			}).encode('utf-8')
			req6 = urllib.request.Request(url=submiturl,data=submitdata,headers=header)
			req6data=urllib.request.urlopen(req6).read().decode("utf-8","ignore")
			
			#订票-第3次post-主要获取Token、leftTicketStr、key_check_isChange、train_location
			initdcurl="https://kyfw.12306.cn/otn/confirmPassenger/initDc"
			initdcdata =urllib.parse.urlencode({
			"_json_att":""
			}).encode('utf-8')
			req7 = urllib.request.Request(url=initdcurl,data=initdcdata,headers=header)
			req7data=urllib.request.urlopen(req7).read().decode("utf-8","ignore")
			
			#如果是学生必须要请求这个
			if isstudent == 'y':
				stuurl = 'https://kyfw.12306.cn/otn/dynamicJs/oorhhvh'
				stureq = urllib.request.Request(url=stuurl,headers=header)
				urllib.request.urlopen(stureq)
				

			#获取train_no、leftTicketStr、fromStationTelecode、toStationTelecode、train_location pattrain_location
			# train_no_pat="'train_no':'(.*?)'"
			# leftTicketStr_pat="'leftTicketStr':'(.*?)'"
			pattoken="var globalRepeatSubmitToken.*?'(.*?)'"
			patkey="'key_check_isChange':'(.*?)'"
			pattrain_location="'tour_flag':'dc','train_location':'(.*?)'"
			
			#train_no
			train_no=train[16]
				
			#leftTicketStr
			leftTicketStr=train[17]

			#fromStationTelecode
			#toStationTelecode	   
			fromStationTelecode = szm[train[1]]
			toStationTelecode = szm[train[2]]
				
			#train_location	   
			train_location=train[18]

			#token	  
			tokenall=re.compile(pattoken).findall(req7data)
			if(len(tokenall)!=0):
				token=tokenall[0]

			#key	
			keyall=re.compile(patkey).findall(req7data)
			if(len(keyall)!=0):
				key=keyall[0]			
			
			#构造pass old
			if pas_old == None:
				pas_old = makePassOld(passengerInfo,checkIndex,thisseats,isstudent)
			passengerTicketStr = pas_old[0]
			oldPassengerStr = pas_old[1]
			
			if(train[setsDetailInfo[thisseats]]=="无" or train[setsDetailInfo[thisseats]]=="*"):
				count = count+1
				print("当前无票，继续监控… 抢票次数："+str(count))
				#time.sleep(0.5)
				continue
			
			#总请求1-点击提交后步骤1-确认订单(在此只定一等座，座位类型为M，如需选择多种类型座位，可以自行修改一下代码使用if判断一下即可)
			checkOrderurl="https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
			checkdata=urllib.parse.urlencode({
			"cancel_flag":2,
			"bed_level_order_num":"000000000000000000000000000000",
			"passengerTicketStr":passengerTicketStr,
			"oldPassengerStr":oldPassengerStr,
			"tour_flag":"dc",
			"randCode":"",
			"whatsSelect":1,
			"_json_att":"",
			"REPEAT_SUBMIT_TOKEN":token,
			}).encode('utf-8')
			req9 = urllib.request.Request(url=checkOrderurl,data=checkdata,headers=header)
			req9data=urllib.request.urlopen(req9).read().decode("utf-8","ignore")
			print("确认订单完成，即将进行下一步")
			
			#总请求2-点击提交后步骤2-获取队列
			getqueurl="https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
			#checkdata=checkOrderdata.encode('utf-8')
			#将日期转为格林时间
			#先将字符串转为常规时间格式
			thisdatestr=date#需要的买票时间
			thisdate=datetime.datetime.strptime(thisdatestr,"%Y-%m-%d").date()
			#再转为对应的格林时间
			gmt='%a+%b+%d+%Y'
			thisgmtdate=thisdate.strftime(gmt)
			
			#将leftstr2转成指定格式
			leftstr2=leftTicketStr.replace("%","%25")
				
			
			getquedata="train_date="+str(thisgmtdate)+"+00%3A00%3A00+GMT%2B0800 (中国标准时间)&train_no="+train_no+"&stationTrainCode="+thiscode+"&seatType="+seatType+"&fromStationTelecode="+fromStationTelecode+"&toStationTelecode="+toStationTelecode+"&leftTicket="+leftstr2+"&purpose_codes="+purpose_codes+"&train_location="+train_location+"&_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)
			getdata=getquedata.encode('utf-8')
			req10 = urllib.request.Request(url=getqueurl,data=getdata,headers=header)
			req10data=urllib.request.urlopen(req10).read().decode("utf-8","ignore")
			print("获取订单队列完成，即将进行下一步")
			
			#总请求3-确认步骤1-配置确认提交
			confurl="https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
			confdata2=urllib.parse.urlencode({
			"passengerTicketStr":passengerTicketStr,
			"oldPassengerStr":oldPassengerStr,
			"randCode":"",
			"purpose_codes":purpose_codes,
			"key_check_isChange":key,
			"leftTicketStr":leftTicketStr,
			"train_location":train_location,
			"choose_seats":"",
			"seatDetailType":"000",
			"whatsSelect":"1",
			"roomType":"00",
			"dwAll":"N",
			"_json_att":"",
			"REPEAT_SUBMIT_TOKEN":token,
			}).encode('utf-8')
			req11 = urllib.request.Request(url=confurl,data=confdata2,headers=header)
			req11data=urllib.request.urlopen(req11).read().decode("utf-8","ignore")
			print("配置确认提交完成，即将进行下一步")
			
			time1=time.time()
			while True:
				#总请求4-确认步骤2-获取orderid
				time2=time.time()
				if((time2-time1)//60>5):
					print("获取orderid超时，正在进行新一次抢购")
					break
				getorderidurl="https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random="+str(int(time.time()*1000))+"&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)
				req12 = urllib.request.Request(url=getorderidurl,headers=header)
				req12data=urllib.request.urlopen(req12).read().decode("utf-8","ignore")
				patorderid='"orderId":"(.*?)"'
				orderidall=re.compile(patorderid).findall(req12data)
				if(len(orderidall)==0):
					print("未获取到orderid，正在进行新一次的请求。")
					continue
				else:
					orderid=orderidall[0]
					break
			print("获取orderid完成，即将进行下一步")
			#总请求5-确认步骤3-请求结果
			resulturl="https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue"
			resultdata="orderSequence_no="+orderid+"&_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)
			resultdata2=resultdata.encode('utf-8')
			req13 = urllib.request.Request(url=resulturl,data=resultdata2,headers=header)
			req13data=urllib.request.urlopen(req13).read().decode("utf-8","ignore")
			print("请求结果完成，即将进行下一步")

			#总请求6-确认步骤4-支付接口页面
			payurl="https://kyfw.12306.cn/otn//payOrder/init"
			paydata="_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)
			paydata2=paydata.encode('utf-8')
			req14 = urllib.request.Request(url=payurl,data=paydata2,headers=header)
			req14data=urllib.request.urlopen(req14).read().decode("utf-8","ignore")
			print("订单已经完成提交，您可以登录后台进行支付了。")
			sends(rec)
			break
		except Exception as e:
			print(e)
			print('****')
			continue


