class Cross:
	def __init__(self, cid,road_id_dict):
		self.cid = cid  # 路口id
		self.road = []  # 存放相连的道路的指针,按照道路升序存放,注意，这个指针只能用来访问信息或调用查询类的方法，但不能进行修改,否则在并行化上会产生问题
		self.road_id_dict = road_id_dict  # 使用字典存放道路的原始顺序{道路id:n}，保留路口的二维信息
		if len(self.road_id_dict)!=0:
			self.road_id_dict2 = dict(zip(self.road_id_dict.values(),self.road_id_dict.keys()))
		print("Cross",cid,"is ok",self.road,self.road_id_dict,self.road_id_dict)

class Road:
	def __init__(self):
		self.r_id=r_id
		self.c_id1=c_id1  		# 路口链接节点1,是一个指针，指向路口c_id1
		self.c_id2=c_id2  		# 路口链接节点2，同理
		self.length=length		# 道路长度
		self.limit=limit        # 道路限速
		self.dir=direction 		# 道路是否可以双向通行
		self.num_way=num_way 	# 几车道
		
		self.r_dict={self.c_id1:self.cap_1,self.c_id2:self.cap_1}  # 该字典说明了路口节点和车道方向的对应关系
		self.cap_1= self.init_capacity()  # 方向1的车道数组
		
		if self.dir==1: # 如果是双向道路
			self.cap_2 = self.init_capacity() # 方向2的车道数组
		else: # 单向道路
			self.cap_2 = None
		print("Road",r_id,"is ok",self.c_id1,' ',self.c_id2,' ',self.length,' ',self.limit,' ',self.dir,' ',self.num_way,' ',self.r_dict)
		

class City_traffic:
	def __init__(self): # 所有路口统一管理的类
		self.all_crosses=[]
		self.all_roads=[]
		self.all_cars=[]

	def second_step_plan(self): 	# 模仿任务书v1.4第22页中系统处理调度逻辑的第二步
		# 7.整个系统调度按路口ID升序进行调度各个路口，路口内各道路按道路ID升序进行调度。每个路口遍历道路时，只调度该道路出路口的方向
		for i in self.all_crosses:
			i.deal_wait_cars()

	def get_cross_path( self , file_path):  #处理路口文件
		with open(file_path) as file_object:
			lines = file_object.readlines()
		print(len(lines))
		for i in range(1, len(lines)):
			One_Cross = lines[i].replace("(", '').replace(",", '').replace(')', '').split()
			myCross=Cross(One_Cross[0],{One_Cross[1]:1,One_Cross[2]:2,One_Cross[3]:3,One_Cross[4]:4})
			# myCross.get_road([One_Cross[1],One_Cross[2],One_Cross[3],One_Cross[4]])
			# self.all_crosses.append(myCross)


	def get_road_path(self, file_path):		#处理道路文件
		with open(file_path) as file_object:
			lines = file_object.readlines()
		print(len(lines))
		for i in range(1, len(lines)):
			One_Road = lines[i].replace("(", '').replace(",", '').replace(')', '').split()
			myRoad = Road(One_Road[0],One_Road[4],One_Road[5], One_Road[1], One_Road[2], One_Road[6], One_Road[3])
			self.all_roads.append(myRoad)


	def search_road_by_id(self,road_id): #road_id 应为'00001'不可以为int型
		for i in self.all_roads:
			if road_id == i.rid:
				return i

#(id,length,speed,channel,from,to,isDuplex) 道路属性
#(id,roadId,roadId,roadId,roadId)  路口属性

cross_path="C:\\Users\\admin\\Desktop\\huawei2019\\cross.txt"
road_path="C:\\Users\\admin\\Desktop\\huawei2019\\road.txt"
city=City_traffic()
city.get_cross_path(cross_path)
city.get_road_path(road_path)