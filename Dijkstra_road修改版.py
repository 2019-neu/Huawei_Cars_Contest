# (id,length,speed,channel,from,to,isDuplex) 道路属性
# (id,roadId,roadId,roadId,roadId)  路口属性
# (id,from,to,speed,planTime)  汽车属性
import operator
import copy


class Car:
    def __init__(self, carid, ffrom, to, speed, planTime):
        self.carid = carid  # 汽车id
        self.speed = None  # 汽车当前行驶速度
        self.ffrom = ffrom  # 汽车的出发路口
        self.tp = to  # 汽车的目的路口
        self.road = None  # 道路指针,指示当前道路
        self.way = None  # 车道索引，指示当前车道
        self.pos = None  # 位置索引，指示当前所在车道的位置
        self.road_plan = []  # 规划的道路列表，存放道路id，
        self.forward = None  # 前车指针，指示前车信息，若无前车，为None
        self.max_speed = speed  # 该汽车的最大限制车速
        self.plan_time = planTime  # 该车的计划出发时间
        self.kind = None  # 0代表车辆等待状态，1代表车辆终止状态

    # print('carid',self.carid,'max_speed',self.max_speed,'plan_time',self.plan_time)

    def __repr__(self):
        return 'CAr\'s id is ' + str(self.carid)


class Cross:
    def __init__(self, cid, cdict1, cdict2, item_cc):
        self.cid = cid  # 路口id
        # self.road = list(cdict1.keys()).sort()  # 存放相连的道路的指针,按照道路升序存放,注意，这个指针只能用来访问信息或调用查询类的方法，但不能进行修改,否则在并行化上会产生问题
        self.road_value_dict = cdict1  # 使用字典存放道路的原始顺序{道路id:n}，保留路口的二维信息
        self.value_road_dict = cdict2
        # print('cid',self.cid,'road',self.road)
        item_cc.sort(key=operator.attrgetter('r_id'))
        # self.road = copy.deepcopy(item_cc)
        self.road = item_cc
        self.adjacent_cross = []

    def Adjacent_Cross(self, cross_item):
        self.adjacent_cross.append(cross_item)

    def get_adj_cross(self):
        for i in range(len(self.adjacent_cross)):
            self.adjacent_cross[i][1]

    def announcement(self):
        for i in range(len(self.road)):
            # print(self)
            self.road[i].answer(self)

    #############################################################################
    # def deal_wait_cars(self):  # 第二步的主步骤，处理该路口的等待车辆下一步的位置
    #     t = 1
    #     while t:  # 直到所有道路都没有等待车辆，或者还有车辆的道路上的第一优先级的车辆处于冲突状态,while循环内是一个时间单位(并行)
    #         topCars = []
    #         for i in range(len(self.road)):
    #             now_car = self.road[i].top_priority(self.cid)  # 获得该道路的最高优先级汽车
    #             if now_car == None:
    #                 t = 0
    #                 break
    #             go_direction = self.judging_direction(now_car)  # 求出该车去向（直行左转右转）
    #             go_road = now_car.road_plan[1]  # 求出该车的下一目的道路id(整数，不是指针)
    #             go_pos =
    #             go_road_value = self.road_id_dict[now_car.road.r_id]
    #             direct_road_value = abs(go_road_value - 2)  #
    #             direct_road_id = self.road_id_dict2[direct_road_value]
    #             if now_car.road.limit <= now_car.speed:
    #                 now_car.speed = now_car.road.limit
    #             elif now_car.road.limit > now_car.speed and now_car.road.limit >= now_car.max_speed:
    #                 now_car.speed = now_car.max_speed
    #             elif now_car.road.limit > now_car.speed and now_car.road.limit < now_car.max_speed:
    #                 now_car.speed = now_car.road.limit
    #             go_distance = self.cal_go_pos(now_car, go_road)
    #             if go_direction == 'D':  # 直行只需要看目标道路是否有空余位置
    #                 if go_distance != 0:
    #                     for j in range(go_distance - 1):
    #                         for k in range(go_distance - 1, -1, -1):
    #                             if roadList[j][k] == 0:  # 道路列表
    #                                 pass  # 下一条道路增加新的车辆(break)  需要在road中增加方法
    #
    #
    #             elif go_direction == 'L':  # 左转要看其右侧车道是否有车辆要直行，同时目标道路要有空位
    #                 go_road_value = self.road_id_dict[now_car.road.r_id]
    #                 right_road_value = (go_road_value - 2) % 4 + 1  #
    #                 right_road_id = self.road_id_dict2[right_road_value]
    #                 right_now_car = self.road[i].top_priority(right_road_id)
    #                 if self.judging_direction(right_now_car) == 'D':
    #                     continue  # 交规冲突，只能等待
    #                 else:
    #                     if go_distance != 0:
    #                         for j in range(go_distance - 1):
    #                             for k in range(go_distance - 1, -1, -1):
    #                                 if roadList[j][k] == 0:  # 道路列表
    #                                     pass  # 下一条道路增加新的车辆(break)
    #
    #             elif go_direction == 'R':  # 右转要看其左侧车道是否有车辆要直行，对面车道是否右侧有左转，同时目标道路要有空位
    #                 go_road_value = self.road_id_dict[now_car.road.r_id]
    #                 left_road_value = go_road_value % 4 + 1  #
    #                 direct_road_value = abs(go_road_value - 2)
    #                 left_road_id = self.road_id_dict2[left_road_value]
    #                 direct_road_id = self.road_id_dict2[direct_road_value]
    #                 left_now_car = self.road[i].top_priority(left_road_id)
    #                 direct_now_car = self.road[i].top_priority(direct_road_id)
    #
    #                 if self.judging_direction(left_now_car) == 'D' or self.judging_direction(direct_now_car) == 'L':
    #                     continue  # 交规冲突，只能等待
    #                 else:
    #                     if go_distance != 0:
    #                         for j in range(go_distance - 1):
    #                             for k in range(go_distance - 1, -1, -1):
    #                                 if roadList[j][k] == 0:  # 道路列表
    #                                     pass  # 下一条道路增加新的车辆(break)
    #
    # def cal_go_pos(self, car, ct, next_road_id):  # 计算car是否可以通过路口，如果可以求出通过路口的理想下一位置（不一定是实际的下一位置）
    #     bow_Mspeed = int(car.road.limit)
    #     next_road = ct.all_roads(next_road_id)
    #     next_Mspeed = int(next_road.limit)
    #
    #     if distance >= next_Mspeed:  # distance：车辆据路口位置,待实现
    #         if bow_Mspeed <= car.limit:
    #             car.speed = car.road.limit
    #         elif car.road.limit > car.speed and car.road.limit >= car.max_speed:
    #             car.speed = car.max_speed
    #         elif car.road.limit > car.speed and car.road.limit < car.max_speed:
    #             car.speed = car.road.limit
    #
    #         return 0
    #     else:
    #         return next_Mspeed - distance
    #
    # def rule(self, rid, goid):  # 交通规则处理函数
    #
    # # 右转，左转比直行优先级低
    # # 右转比左转优先级低
    # # 右转
    #
    # def judging_direction(self, car):  # 根据所在道路id和下一个道路id判断汽车是直行，左转，还是右转
    #     nowid = self.road_id_dict[car.road_plan[0]]
    #     nextid = self.road_id_dict[car.road_plan[1]]
    #     if abs(nextid - nowid) == 2:  # 直行
    #         return 'D'
    #     elif [nextid, nowid] in [[4, 1], [2, 3], [1, 2], [3, 4]]:  # 右转
    #         return 'R'
    #     else:
    #         return 'L'
    #
    # def notice_road(self):  # 向道路发出通知，一辆汽车已经驶入你所在的路段
    #     pass
    #############################################################################


    def __repr__(self):
        return 'Cross\'s id is ' + str(self.cid)




class Road:
    def __init__(self, r_id, c_id1, c_id2, length, limit, direction, num_way):
        self.r_id = r_id
        self.c_id1 = None  # 路口链接节点1指针,指向路口c_id1,起始点id
        self.c_id2 = None  # 路口链接节点2指针，结束点id
        self.cid1 = c_id1  # 入口路口id，int型
        self.cid2 = c_id2  # 出口路口id，int型
        self.cdict = {c_id1: 1, c_id2: 2}
        self.length = length  # 道路长度
        self.limit = limit  # 道路限速
        self.dir = direction  # 道路是否可以双向通行
        self.num_way = num_way  # 几车道
        self.cap_1 = self.init_capacity()  # 方向1的车道数组
        if self.dir == 1:  # 如果是双向道路
            self.cap_2 = self.init_capacity()  # 方向2的车道数组
            self.r_dict = {c_id1: self.cap_1,
                           c_id2: self.cap_2}  # 该字典说明了路口节点和车道方向的对应关系，从起始点进入的车辆都在cap_1，从终止点进入的车辆都在cap_2
        else:  # 单向道路
            self.cap_2 = None
            self.r_dict = {c_id1: self.cap_1}

    # print("Road",r_id,"is ok",'Enter id',self.c_id1,'Out id',self.c_id2,'length',self.length,'limit',self.limit,'double',self.dir,'way_nums',self.num_way)

    def init_capacity(self):  # 为道路初始化道路空间,是一个n*m维的数组
        return [[0] * self.length for i in range(self.num_way)]

    def answer(self, one_cross):  # 该方法被路口所调用，用以接受路口指针
        wh = self.cdict[one_cross.cid]  # 判断是入口路口还是出口路口
        # print('wh',wh)
        if wh == 1:
            self.c_id1 = one_cross
           # print(self.c_id1)
        else:
            self.c_id2 = one_cross
         #   print(self.c_id2)

    def Announcement_Adjacent_Cross(self):  # 通知与该道路相连的路口，其相邻的路口是什么
        self.c_id1.Adjacent_Cross([self.length, self.c_id2.cid])
        self.c_id2.Adjacent_Cross([self.length, self.c_id1.cid])

    def scanner_wait_cars(self):  # 第一步的主步骤，扫描本道路的所有等待车辆,为各车辆确定属性
        for l in range(len(self.r_dict)):
            cap = self.r_dict[list(self.r_dict.keys())][l]
            for i in range(len(cap)):  # 扫描道路
                print('self.r_dict[list(self.r_dict.keys())[l]]', self.r_dict[list(self.r_dict.keys())[l]])
                for j in range(len(cap[i]) - 1, -1, -1):  # 逆序扫描车道
                    if cap[i][j] == None:
                        continue  # 该路段位置无车
                    else:
                        if cap[i][j].forward == None:  # 该汽车前面无车
                            pass
                        else:  # 该汽车前面有车
                            if cap[i][j].forward.kind == 0:  # 如果前车是等待状态车
                                if self.spacing(cap[i][j], cap[i][j].forward) < min(self.limit,
                                                                                    cap[i][j].max_speed):  # 对应实现第一步的c)
                                    cap[i][j].kind = 0  # 此时该车满足等待条件，也成为等待车辆
                            else:
                                cap[i][j].kind = 0  # 不满足等待条件为终止车辆
                                cap[i][j].speed = self.determine_MaxCarSpeed(cap[i][j])  # 为终止状态车辆确定当前速度
                                cap[i][j].pos += cap[i][j].speed  # 跟新终止状态车辆的位置(终止状态车辆的位置是否会越界？)

    # 求一辆汽车距离路口还有多远
    def cal_dis_cross(self):
        pass

    def __repr__(self):
        return 'Road\'s id is ' + str(self.r_id)
    #############################################################################
    # def notice_cross(self):  # 向道路发出通知，一辆汽车已经驶入你所在的路口
    #     pass
    #
    # def add_car(self, car, cross_id, way_id, long):  # 加入一辆汽车
    #     # 参数car加入的汽车指针; cross_id汽车从哪一个路口驶入; way_id汽车驶入了哪一个车道; long 汽车已经在本路段行驶了多远
    #     self.r_dict[cross_id][way_id][long] = car  # 注意数组不要越界！！,将该汽车加入到该路段的相应位置
    #
    # def block(self, posb, posf, maxv):  # 判断前车是否阻挡后车
    #     # posf,posb前后车位置,maxv最大限速
    #     if (posf - posb) < maxv:
    #         return True
    #     else:
    #         return False
    #
    # def pass_cross(self):  # 检查车道中的某一辆车是否可以通过路口
    #     pass
    #
    # def spacing(self, a, b):  # 求a,b两车的间距,a为后车，b为前车
    #     if a.road != b.road or a.way != b.way:
    #         return None
    #     else:
    #         return (b.pos - a.pos)
    #
    # def determine_MaxCarSpeed(self, a):  # 根据前车信息确定当前车辆a的最大可行驶速度，该函数只能处理终止状态的汽车
    #     if a.forward == None:  # 车辆a无前车,其可行驶的最大速度为min(a.max_speed,self.limit)
    #         return min(a.max_speed, self.limit)
    #     else:  # 有前车
    #         return min(a.max_speed, self.limit, spacing(a,
    #                                                     a.forward))  # 注意公式为什么是v = min(最高车速，道路限速，s/t)而不是v = min(最高车速，道路限速，(a.forward.speed-s)/t),注意我们之前说的变速规则是不对的！！！
    #
    # def top_priority(self, cid):  # 返回该与道路连接的路口id为cid方向上最大通行优先级的车辆
    #     for j in range(self.num_way):  # 遍历车道的列
    #         for i in range(len(self.r_dict[cid]) - 1, -1, -1):  # 逆序遍历扫描车道的行(即安装任务书中给出的蛇形轨迹进行扫描)
    #             if self.r_dict[cid][i][j] != None and self.r_dict[cid][i][j].kind == 0:  # 短路，不为空且为等待状态车辆
    #                 return self.r_dict[cid][i][j]
    #     return None  # 该道路上没有车辆行驶
    #############################################################################



class City_traffic:
    def __init__(self):  # 所有路口统一管理的类
        self.all_crosses = []
        self.all_roads = []
        self.all_cars = []
        self.road_map = {}  # 道路id与道路指针之间的map
        self.cross_map = {}  # 路口id与路口指针之间的map
        self.car_map = {}  # 汽车id与汽车指针之间的map
        self.graph = None  # 邻接矩阵,矩阵的节点顺序和all_crosses一致
        self.graph_map = {}

    def make_map(self):
        dd = float("inf")
        line = [dd] * len(self.all_crosses)
        graph = []
        for i in range(len(self.all_crosses)):
            graph.append(line[:])
            self.graph_map.update({self.all_crosses[i].cid: i})
        graph = np.array(graph)
        print(graph)
        for i in range(len(graph)):
            graph[i][i] = 0
        return graph

    def second_step_plan(self):  # 模仿任务书v1.4第22页中系统处理调度逻辑的第二步
        # 7.整个系统调度按路口ID升序进行调度各个路口，路口内各道路按道路ID升序进行调度。每个路口遍历道路时，只调度该道路出路口的方向
        for i in self.all_crosses:
            i.deal_wait_cars()

    def get_road_path(self, file_path):  # 处理道路文件
        with open(file_path) as file_object:
            lines = file_object.readlines()
        # print(len(lines))
        for i in range(1, len(lines)):
            One_Road = list(map(int, lines[i].replace("(", '').replace(",", '').replace(')', '').split()))
            # print(One_Road)
            myRoad = Road(One_Road[0], One_Road[4], One_Road[5], One_Road[1], One_Road[2], One_Road[6], One_Road[3])
            self.road_map.update({One_Road[0]: myRoad})
            self.all_roads.append(myRoad)

    def get_cross_path(self, file_path):  # 处理路口文件
        with open(file_path) as file_object:
            lines = file_object.readlines()
        # print(len(lines))
        for i in range(1, len(lines)):
            One_Cross = list(map(int, lines[i].replace("(", '').replace(",", '').replace(')', '').split()))
            cid = One_Cross.pop(0)
            cdict1, cdict2, item_cc = {}, {}, []
            for i in range(len(One_Cross)):
                if One_Cross[i] != -1:
                    cdict1.update({One_Cross[i]: i + 1})
                    cdict2.update({i + 1: self.road_map[One_Cross[i]]})  # 每一个路口首先建立起与道路指针的联系
                    item_cc.append(self.road_map[One_Cross[i]])
            myCross = Cross(cid, cdict1, cdict2, item_cc)
            myCross.announcement()
            self.all_crosses.append(myCross)
            self.cross_map.update({cid: myCross})

    def get_car_path(self, file_path):  # 处理车辆文件
        with open(file_path) as file_object:
            lines = file_object.readlines()
        for i in range(1, len(lines)):
            One_car = list(map(int, lines[i].replace("(", '').replace(",", '').replace(')', '').split()))
            mycar = Car(One_car[0], One_car[1], One_car[2], One_car[3], One_car[4])
            self.car_map.update({One_car[0]: mycar})
            self.all_cars.append(mycar)

    def Make_Adj(self):
        for i in range(len(self.all_roads)):
            self.all_roads[i].Announcement_Adjacent_Cross()


# 测试指针是否赋值正常
#for i in range(len(city.all_crosses)):
#    print('cross', city.all_crosses[i].cid, 'cid is :', city.all_crosses[i].road)

# 测试指针是否赋值正常
#for i in range(len(city.all_roads)):
#    print('road', city.all_roads[i].r_id, 'from:', city.all_roads[i].c_id1.cid, 'to', city.all_roads[i].c_id2.cid)

cross_path = "cross.txt"
road_path = "road.txt"
car_path = "car.txt"
city = City_traffic()
city.get_road_path(road_path)
city.get_cross_path(cross_path)
city.Make_Adj()  # 建立路口与路口之间的相邻关系
city.get_car_path(car_path)
file_result=[]


class Vertex:
    #顶点类
    def __init__(self,cross_id,item):
        self.vid = cross_id#出边
        self.outList = item #出边指向的顶点id的列表，也可以理解为邻接表
        self.know = False#默认为假
        self.dist = float('inf')#s到该点的距离,默认为无穷大
        self.prev = 0#上一个顶点的id，默认为0
        self.cross_rid=[]
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.vid == other.vid
        else:
            return False
    def __hash__(self):
        return hash(self.vid)

# one_cross=city.all_crosses.pop(0)
# one_item=[]
# for i in one_cross.road_value_dict.keys():
#     if city.road_map[i].cid1 == one_cross.cid:
#         one_item.append(int(city.road_map[i].cid2))
#     elif city.road_map[i].cid2 == one_cross.cid and city.road_map[i].dir == 1:
#         one_item.append(city.road_map[i].cid1)
# v1=Vertex(int(one_cross.cid),one_item)
#创建一个长度为8的数组，来存储顶点，0索引元素不存
relist = [False]
#使用set代替优先队列，选择set主要是因为set有方便的remove方法
reset = set([])

while city.all_crosses:
    every_cross=city.all_crosses.pop(0)
    every_item=[]
    for i in every_cross.road_value_dict.keys():
        if city.road_map[i].cid1 == every_cross.cid:
            every_item.append(city.road_map[i].cid2)
        elif city.road_map[i].cid2 ==every_cross.cid and city.road_map[i].dir == 1:
            every_item.append(city.road_map[i].cid1)
    relist.append(Vertex(int(every_cross.cid),every_item))
    reset.add(Vertex(int(every_cross.cid),every_item))

edges_road_id=dict()
edges = dict()
def add_edge(front,back,value):
    edges[(front,back)]=value

# def add_edge_rid(front,back,value):
#     edges[(front,back)]=value

while city.all_roads:
    every_road=city.all_roads.pop(0)
    if every_road.dir==1:
        add_edge(int(every_road.cid1), int(every_road.cid2), [int(every_road.length),every_road.r_id])
        add_edge(int(every_road.cid2), int(every_road.cid1), [int(every_road.length),every_road.r_id])
        # add_edge_rid(int(every_road.cid1), int(every_road.cid2),every_road.r_id)
        # add_edge_rid(int(every_road.cid2), int(every_road.cid1), every_road.r_id)
    else:
        add_edge(int(every_road.cid1), int(every_road.cid2), [int(every_road.length),every_road.r_id])
        # add_edge_rid(int(every_road.cid1), int(every_road.cid2), every_road.r_id)

def get_unknown_min(gvlist,gvset):#此函数则代替优先队列的出队操作
    the_min = 0
    the_index = 0
    j = 0
    for i in range(1,len(gvlist)):
        if(gvlist[i].know is True):
            continue
        else:
            if(j==0):
                the_min = gvlist[i].dist
                the_index = i
            else:
                if(gvlist[i].dist < the_min):
                    the_min = gvlist[i].dist
                    the_index = i
            j += 1
    #此时已经找到了未知的最小的元素是谁
    gvset.remove(gvlist[the_index])#相当于执行出队操作
    return gvlist[the_index]


def main(dd,mvlist,mvset):
    #将v1设为顶点
    mvlist[dd].dist = 0
    while(len(mvset)!=0):
        v = get_unknown_min(mvlist,mvset)
        # print(v.vid,v.dist,v.outList)
        v.know = True
        for w in v.outList:#w为索引
            if(mvlist[w].know is True):
                continue
            if(mvlist[w].dist == float('inf')):

                mvlist[w].dist = v.dist + edges[(v.vid,w)][0]
                # mvlist[w].cross_rid.append(edges[(v.vid,w)][1])
                mvlist[w].prev = v.vid
            else:
                if((v.dist + edges[(v.vid,w)][0])<mvlist[w].dist):
                    mvlist[w].dist = v.dist + edges[(v.vid,w)][0]
                    # mvlist[w].cross_rid.append(edges[(v.vid, w)][1])
                    mvlist[w].prev = v.vid
                else:#原路径长更小，没有必要更新
                    pass

def real_get_traj(start,index_main, vvlist):
    traj_list = [start.carid]
    def get_traj(index):#参数是顶点在vlist中的索引
        if(index == start.ffrom):#终点
            # traj_list.append(index)
            # traj_list.append(start.carid)
            # file_result.append(traj_list[::-1])#反转list
            # print(file_result)
            return
        if(vvlist[index].dist == float('inf')):
            print('从起点到该顶点根本没有路径')
            return

        # traj_list.append(index)
        # all_id.append(edges[()])
        get_traj(vvlist[index].prev)
        traj_list.append(edges[(vvlist[index].prev,index)][1])
        # print(str(vvlist[index].prev)+'..'+str(index)+'..'+str(edges[(vvlist[index].prev,index)][1]))
    get_traj(index_main)
    file_result.append(traj_list)

while city.all_cars:
    one_car=city.all_cars.pop(0)
    vlist =copy.deepcopy(relist)
    vset = copy.deepcopy(reset)
    main(one_car.ffrom,vlist,vset)
    real_get_traj(one_car, one_car.tp, vlist)


with open('answer.txt','w') as write_file:
    write_file.write("#(carId,RoadId...)"+'\n')
    for list in file_result:
        write_file.write(str(list) + '\n')