#(id,length,speed,channel,from,to,isDuplex) 道路属性
#(id,roadId,roadId,roadId,roadId)  路口属性
#(id,from,to,speed,planTime)  汽车属性
import operator
#import numpy as np


class Car:
	def __init__(self,carid,ffrom,to,speed,planTime):
		self.carid = carid				# 汽车id
		self.speed = None				# 汽车当前行驶速度
		self.ffrom=ffrom				# 汽车的出发路口
		self.tp=to						# 汽车的目的路口
		self.road = None				# 道路指针,指示当前道路
		self.way = None 				# 车道索引，指示当前车道
		self.pos = None					# 位置索引，指示当前所在车道的位置
		self.road_plan = []  			# 规划的道路列表，存放道路id，
		self.forward = None 			# 前车指针，指示前车信息，若无前车，为None
		self.max_speed = speed 			# 该汽车的最大限制车速
		self.plan_time=planTime 		#该车的计划出发时间
		self.kind = None 				# 0代表车辆等待状态，1代表车辆终止状态
		#print('carid',self.carid,'max_speed',self.max_speed,'plan_time',self.plan_time)
	
	def __repr__(self):
		return 'CAr\'s id is '+str(self.carid)
	
	
class Cross:
	def __init__(self, cid,cdict1,cdict2,item_cc):
		self.cid = cid  # 路口id
		#self.road = list(cdict1.keys()).sort()  # 存放相连的道路的指针,按照道路升序存放,注意，这个指针只能用来访问信息或调用查询类的方法，但不能进行修改,否则在并行化上会产生问题
		self.road_value_dict = cdict1  # 使用字典存放道路的原始顺序{道路id:n}，保留路口的二维信息
		self.value_road_dict= cdict2
		#print('cid',self.cid,'road',self.road)
		item_cc.sort(key=operator.attrgetter('r_id'))
		# self.road = copy.deepcopy(item_cc)
		self.road = item_cc
		self.adjacent_cross=[]
	
	def Adjacent_Cross(self,cross_item):
		self.adjacent_cross.append(cross_item)
		
		
	def get_adj_cross(self):
		for i in range(len(self.adjacent_cross)):
			self.adjacent_cross[i][1]
		
	def announcement(self):
		for i in range(len(self.road)):
			#print(self)
			self.road[i].answer(self)
			
	def __repr__(self):
		return 'Cross\'s id is '+str(self.cid)
			
			
class Road:
	def __init__(self,r_id,c_id1,c_id2,length,limit,direction,num_way):
		self.r_id=r_id
		self.c_id1=None  		# 路口链接节点1指针,指向路口c_id1,起始点id
		self.c_id2=None  		# 路口链接节点2指针，结束点id
		self.cid1=c_id1			# 入口路口id，int型
		self.cid2=c_id2			# 出口路口id，int型
		self.cdict={c_id1:1,c_id2:2}	
		self.length=length		# 道路长度
		self.limit=limit        # 道路限速
		self.dir=direction 		# 道路是否可以双向通行
		self.num_way=num_way 	# 几车道
		self.cap_1= self.init_capacity()  # 方向1的车道数组
		if self.dir==1: # 如果是双向道路
			self.cap_2 = self.init_capacity() # 方向2的车道数组
			self.r_dict={c_id1:self.cap_1,c_id2:self.cap_2}  # 该字典说明了路口节点和车道方向的对应关系，从起始点进入的车辆都在cap_1，从终止点进入的车辆都在cap_2
		else: # 单向道路
			self.cap_2 = None
			self.r_dict={c_id1:self.cap_1}
		#print("Road",r_id,"is ok",'Enter id',self.c_id1,'Out id',self.c_id2,'length',self.length,'limit',self.limit,'double',self.dir,'way_nums',self.num_way)
		
	def init_capacity(self):  # 为道路初始化道路空间,是一个n*m维的数组
		return [[0] * self.length for i in range(self.num_way)]
	
	def answer(self,one_cross):  			#该方法被路口所调用，用以接受路口指针
		wh=self.cdict[one_cross.cid]		#判断是入口路口还是出口路口
		#print('wh',wh)
		if wh==1:
			self.c_id1=one_cross
			print(self.c_id1)
		else:
			self.c_id2=one_cross
			print(self.c_id2)
			 
	def Announcement_Adjacent_Cross(self): #通知与该道路相连的路口，其相邻的路口是什么
		self.c_id1.Adjacent_Cross([self.length,self.c_id2.cid])
		self.c_id2.Adjacent_Cross([self.length,self.c_id1.cid])
		
	
	def scanner_wait_cars(self): # 第一步的主步骤，扫描本道路的所有等待车辆,为各车辆确定属性
		for l in range(len(self.r_dict)):
			cap=self.r_dict[list(self.r_dict.keys())][l]
			for i in range(len(cap)): # 扫描道路
				print('self.r_dict[list(self.r_dict.keys())[l]]',self.r_dict[list(self.r_dict.keys())[l]])
				for j in range(len(cap[i])-1,-1,-1): # 逆序扫描车道
					if cap[i][j]==None:
						continue # 该路段位置无车
					else:
						if cap[i][j].forward==None:	# 该汽车前面无车
							pass
						else:  # 该汽车前面有车
							if cap[i][j].forward.kind==0:  # 如果前车是等待状态车
								if self.spacing(cap[i][j],cap[i][j].forward)< min(self.limit,cap[i][j].max_speed):	 # 对应实现第一步的c)
									cap[i][j].kind=0 # 此时该车满足等待条件，也成为等待车辆
							else:
								cap[i][j].kind=0 # 不满足等待条件为终止车辆
								cap[i][j].speed = self.determine_MaxCarSpeed(cap[i][j]) # 为终止状态车辆确定当前速度
								cap[i][j].pos += cap[i][j].speed # 跟新终止状态车辆的位置(终止状态车辆的位置是否会越界？)
				
	# 求一辆汽车距离路口还有多远
	def cal_dis_cross(self):
		pass
		
	def __repr__(self):
		return 'Road\'s id is '+str(self.r_id)
	
	
class City_traffic:
	def __init__(self): # 所有路口统一管理的类
		self.all_crosses=[]
		self.all_roads=[]
		self.all_cars=[]
		self.road_map={}			#道路id与道路指针之间的map
		self.cross_map={}			#路口id与路口指针之间的map
		self.car_map={}				#汽车id与汽车指针之间的map
		self.graph=None				#邻接矩阵,矩阵的节点顺序和all_crosses一致
		self.graph_map={}			

	def make_map(self):
		dd = float("inf")
		line=[dd]*len(self.all_crosses)
		graph=[]
		for i in range(len(self.all_crosses)):
			graph.append(line[:])
			self.graph_map.update({self.all_crosses[i].cid:i})
		graph=np.array(graph)
		print(graph)
		for i in range(len(graph)):
			graph[i][i]=0
		return graph
		
		
	def second_step_plan(self): 	# 模仿任务书v1.4第22页中系统处理调度逻辑的第二步
		# 7.整个系统调度按路口ID升序进行调度各个路口，路口内各道路按道路ID升序进行调度。每个路口遍历道路时，只调度该道路出路口的方向
		for i in self.all_crosses:
			i.deal_wait_cars()
			
	
	def get_road_path(self, file_path):		#处理道路文件
		with open(file_path) as file_object:
			lines = file_object.readlines()
		#print(len(lines))
		for i in range(1, len(lines)):
			One_Road = list(map(int,lines[i].replace("(", '').replace(",", '').replace(')', '').split()))
			#print(One_Road)
			myRoad = Road(One_Road[0],One_Road[4],One_Road[5], One_Road[1], One_Road[2], One_Road[6], One_Road[3])
			self.road_map.update({One_Road[0]:myRoad})
			self.all_roads.append(myRoad)
			
			
	def get_cross_path( self , file_path):  #处理路口文件
		with open(file_path) as file_object:
			lines = file_object.readlines()
		#print(len(lines))
		for i in range(1, len(lines)):
			One_Cross = list(map(int,lines[i].replace("(", '').replace(",", '').replace(')', '').split()))
			cid=One_Cross.pop(0)
			cdict1,cdict2,item_cc={},{},[]
			for i in range(len(One_Cross)):
				if One_Cross[i]!=-1:
					cdict1.update({One_Cross[i]:i+1})
					cdict2.update({i+1:self.road_map[One_Cross[i]]})  #每一个路口首先建立起与道路指针的联系
					item_cc.append(self.road_map[One_Cross[i]])
			myCross=Cross(cid,cdict1,cdict2,item_cc)
			myCross.announcement()
			self.all_crosses.append(myCross)
			self.cross_map.update({cid:myCross})
	
	
	def get_car_path( self , file_path):  #处理车辆文件
		with open(file_path) as file_object:
			lines = file_object.readlines()
		for i in range(1, len(lines)):
			One_car = list(map(int,lines[i].replace("(", '').replace(",", '').replace(')', '').split()))
			mycar=Car(One_car[0],One_car[1],One_car[2],One_car[3],One_car[4])
			self.car_map.update({One_car[0]:mycar})
			self.all_cars.append(mycar)
	
	def Make_Adj(self):
		for i in range(len(self.all_roads)):
			self.all_roads[i].Announcement_Adjacent_Cross()
			
	

			
		

cross_path="C:\\Users\\admin\\Desktop\\huawei2019\\cross.txt"
road_path="C:\\Users\\admin\\Desktop\\huawei2019\\road.txt"
car_path="C:\\Users\\admin\\Desktop\\huawei2019\\car.txt"
city=City_traffic()
city.get_road_path(road_path)
city.get_cross_path(cross_path)
city.Make_Adj()  #建立路口与路口之间的相邻关系
city.get_car_path(car_path)

# 测试指针是否赋值正常
for i in range(len(city.all_crosses)):
	print('cross',city.all_crosses[i].cid,'cid is :',city.all_crosses[i].road)

# 测试指针是否赋值正常
for i in range(len(city.all_roads)):
	print('road',city.all_roads[i].r_id,'from:',city.all_roads[i].c_id1.cid,'to',city.all_roads[i].c_id2.cid)



