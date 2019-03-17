import SDK_python


class kindError(Exception):   #自定义异常类,所有与车辆状态错误导致的异常
    def __init__(self,ErrorInfo):
        super().__init__(self) #初始化父类
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.errorinfo
    
# if __name__ == '__main__':
    # try:
        # raise CustomError('客户异常')
    # except CustomError as e:
        # print(e)
		
		
class Car:
    def __init__(self):
        self.cid = cid              # 汽车id
        self.speed = speed			# 汽车当前行驶速度
        self.road = road   			# 道路指针,指示当前道路
		self.way = way				# 车道索引，指示当前车道
		self.pos = pos				# 位置索引，指示当前所在车道的位置
        self.road_plan = []  		# 规划的道路列表，存放道路id，
        self.forward = forward 		# 前车指针，指示前车信息，若无前车，为None
        self.max_speed = max_speed 	# 该汽车的最大限制车速
		self.kind = 0 				# 0代表车辆等待状态，1代表车辆终止状态

    def change_speed(self):  # 控制车速,当前车速由前车车速，道路限速，汽车极限速度三者共同决定
        # speed change

    def ask_forward(self): # 询问当前道路前车信息
        self.forward=self.road.answer(self)  # 返回前车信息

    def run(self):  #改变位置
        self.road.change_pos(self)  # 通知道路改变该车辆位置

    def plan(self):  # 路径规划方法，为汽车规划路线
        pass
	
	def next_road(self):  # 向路口报告该车下一个路口的去向
		return self.road_plan[1]
	
    def change_road(self,road): # 汽车经过路口，更新车辆状态
        self.road_plan.pop(0)   # 删除已经走过的道路
        self.road=road          # 指向新的道路指针
        self.ask_forward()         # 询问新的前车信息,更新前车指针


class Roads:
    def __init__(self): # 所有道路统一管理的类
        self.all_roads=[]
		self.all_roads_dict={rid:road1}  # 根据道路id快速检索到目标道路的指针
	
	
	def seach(self,road): #根据道路road_id检索到目标道路的指针
		return self.all_roads_dict[road]

		
	def first_step_plan(self ):  # 模仿任务书v1.4第22页中系统处理调度逻辑的第一步
		for i in  range(len(self.all_roads)): # 该步骤处理所有道路的车辆的顺序，不影响其他道路上车辆的顺序，因此先调度哪条道路无关紧要
			self.all_roads[i].scanner_wait_cars()  # 扫描本道路的所有等待汽车
		
	def seach(self,road): #根据道路road_id检索到目标道路的指针
		return self.all_roads_dict[road]
			
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
			
		
    def init_capacity(self):  # 为道路初始化道路空间,是一个n*m维的数组
        return [[0] * self.length for i in range(self.num_way)]

    def notice_cross(self): # 向道路发出通知，一辆汽车已经驶入你所在的路口
        pass

    def add_car(self,car,cross_id,way_id,long): # 加入一辆汽车
        # 参数car加入的汽车指针; cross_id汽车从哪一个路口驶入; way_id汽车驶入了哪一个车道; long 汽车已经在本路段行驶了多远
        self.r_dict[cross_id][way_id][long]=car   # 注意数组不要越界！！,将该汽车加入到该路段的相应位置

    def answer(self,car): # 返回询问汽车的前车信息
        pass
	
	def scanner_wait_cars(self): # 第一步的主步骤，扫描本道路的所有等待车辆,为各车辆确定属性
		for i in range(len(self.cap_1)): # 扫描道路
			for j in range(len(self.cap_1[i])-1,-1,-1): # 逆序扫描车道
				if self.cap_1[i][j]==None:
					continue # 该路段位置无车
				else:
					if self.cap_1[i][j].forward==None:  # 该汽车前面无车
						pass
					else:  # 该汽车前面有车
						if self.cap_1[i][j].forward.kind==0:  # 如果前车是等待状态车
							if self.spacing(self.cap_1[i][j],self.cap_1[i][j].forward)< min(self.limit,self.cap_1[i][j].max_speed):  # 对应实现第一步的c)
								self.cap_1[i][j].kind=0 # 此时该车满足等待条件，也成为等待车辆
						else:
							self.cap_1[i][j].kind=0 # 不满足等待条件为终止车辆
							self.cap_1[i][j].speed = self.determine_MaxCarSpeed(self.cap_1[i][j]) # 为终止状态车辆确定当前速度
							self.cap_1[i][j].pos += self.cap_1[i][j].speed # 跟新终止状态车辆的位置(终止状态车辆的位置是否会越界？)
					
				
	def block(self,posb,posf,maxv): # 判断前车是否阻挡后车
		# posf,posb前后车位置,maxv最大限速
		if (posf-posb)<maxv:
			return True
		else:
			return False
				 
	def pass_cross(self): # 检查车道中的某一辆车是否可以通过路口
		pass
	
	def spacing(self,a,b): # 求a,b两车的间距,a为后车，b为前车
		if a.road!=b.road or a.way != b.way :
			return None
		else:
			return (b.pos-a.pos)
			
	def determine_MaxCarSpeed(self,a):  	# 根据前车信息确定当前车辆a的最大可行驶速度，该函数只能处理终止状态的汽车
		if a.forward==None:	# 车辆a无前车,其可行驶的最大速度为min(a.max_speed,self.limit)
			return min(a.max_speed,self.limit)
		else:  # 有前车
			return min(a.max_speed,self.limit,spacing(a,a.forward))  # 注意公式为什么是v = min(最高车速，道路限速，s/t)而不是v = min(最高车速，道路限速，(a.forward.speed-s)/t),注意我们之前说的变速规则是不对的！！！
			
	
	def top_priority(self,cid): # 返回该与道路连接的路口id为cid方向上最大通行优先级的车辆
		for j in range(self.num_way): # 遍历车道的列
			for i in range(len(self.r_dict[cid])-1,-1,-1): # 逆序遍历扫描车道的行(即安装任务书中给出的蛇形轨迹进行扫描)
				if self.r_dict[cid][i][j] !=None and  self.r_dict[cid][i][j].kind==0 : #短路，不为空且为等待状态车辆
					return self.r_dict[cid][i][j]
		return None  #该道路上没有车辆行驶 
			


class City_traffic:
    def __init__(self): # 所有路口统一管理的类
        self.all_crosses=[]
        self.all_roads=[]
        self.all_cars=[]

    def second_step_plan(self): 	# 模仿任务书v1.4第22页中系统处理调度逻辑的第二步
        # 7.整个系统调度按路口ID升序进行调度各个路口，路口内各道路按道路ID升序进行调度。每个路口遍历道路时，只调度该道路出路口的方向
        for i in range(len(self.all_crosses)):
            if self.all_crosses[i]:
                Cross.()


    def get_file_path(self,file_path,roads):
        with open(file_path) as file_object:
            lines = file_object.readlines()

        for i in range(1, len(lines)):
            One_Cross = lines[i].replace("(", '').replace(",", '').replace(')', '').split()
            myCross=Cross(One_Cross[0])
            myCross.road_id_dict={One_Cross[1]:1,One_Cross[2]:2,One_Cross[3]:3,One_Cross[4]:4}
            myCross.get_road([One_Cross[1],One_Cross[2],One_Cross[3],One_Cross[4]])
            self.all_crosses.append(myCross)


			
	
class Cross:
    def __init__(self,cid):
		self.cid=cid # 路口id
        self.road=[] # 存放相连的道路的指针,按照道路升序存放,注意，这个指针只能用来访问信息或调用查询类的方法，但不能进行修改,否则在并行化上会产生问题
		self.road_id_dict={rcd1:1,rcd1:2,rcd1:3,rcd1:4} # 使用字典存放道路的原始顺序{道路id:n}，保留路口的二维信息
		
		
	def seach_road(self,rid): #根据道路id获得道路指针
		for i in range(len(self.road)

	def deal_wait_cars(self):   # 第二步的主步骤，处理该路口的等待车辆下一步的位置
		while True: 			# 直到所有道路都没有等待车辆，或者还有车辆的道路上的第一优先级的车辆处于冲突状态,while循环内是一个时间单位(并行)
			topCars=[] 
			for i in range(len(self.road)):
				now_car=self.road[i].top_priority(self.cid)  # 获得该道路的最高优先级汽车
				go_direction=self.judging_direction(now_car) #求出该车去向（直行左转右转）
				go_road=now_car.road_plan[1] # 求出该车的下一目的道路id(整数，不是指针)
				go_pos=
				if go_direction=='D': # 直行只需要看目标道路是否有空余位置
					pass
				elif go_direction=='L':  # 左转要看其右侧车道是否有车辆要直行，同时目标道路要有空位
					pass
				elif go_direction=='R':	# 右转要看其左侧车道是否有车辆要直行，对面车道是否右侧有左转，同时目标道路要有空位
					pass
	
	def cal_go_pos(self,car): #计算car是否可以通过路口，如果可以求出通过路口的理想下一位置（不一定是实际的下一位置）
		bow_Mspeed,next_Mspeed=car.road.limit
		
		
	def rule(self,rid,goid): # 交通规则处理函数
		# 右转，左转比直行优先级低
		# 右转比左转优先级低
		# 右转
	
	def judging_direction(self,car): #根据所在道路id和下一个道路id判断汽车是直行，左转，还是右转
		nowid=self.road_id_dict[car.road_plan[0]]
		nextid=self.road_id_dict[car.road_plan[1]]
		if abs(nextid-nowid)==2: #直行
			return 'D'
		elif [nextid,nowid] in [[4,1],[2,3],[1,2],[3,4]]: # 右转
			return 'R'
		else:
			return 'L'
			
	
    def notice_road(self):  # 向道路发出通知，一辆汽车已经驶入你所在的路段
        pass


def get_road(self, roads):
	while roads:
		if min(roads) != -1:
			self.road.append(self.seach_road(min(roads)))
			roads.pop(roads.index(min(roads)))

		
		
		
