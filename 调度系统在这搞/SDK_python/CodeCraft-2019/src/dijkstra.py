def real_get_traj(start, index_main, vvlist, edges):
    traj_list = [start.carid]
    traj_list.insert(1, start.plan_time)  # 增加车辆的调度时间，方便输出answer
    # print(vvlist[1].outList)
    def get_traj(index):  # 参数是顶点在vlist中的索引
        if (index == start.ffrom):  # 终点
            # traj_list.append(index)
            # traj_list.append(start.carid)
            # file_result.append(traj_list[::-1])#反转list
            # print(file_result)
            return
        if (vvlist[index].dist == float('inf')):
            print('从起点到该顶点根本没有路径')
            return

        # traj_list.append(index)
        # all_id.append(edges[()])
        get_traj(vvlist[index].prev)
        traj_list.append(edges[(vvlist[index].prev, index)][1])
    # print(str(vvlist[index].prev)+'..'+str(index)+'..'+str(edges[(vvlist[index].prev,index)][1]))
    get_traj(index_main)
    # file_result.append(traj_list)
    return traj_list



def dj(dd, mvlist, mvset, edges):
    # 将dd(crossid)设为顶点,dist为每路口到顶点的距离
    mvlist[dd].dist = 0
    # mvset中为未规划距的点
    while (len(mvset) != 0):
        # 获得各个点距出发点的最近距离
        def get_unknown_min(gvlist, gvset):  # 此函数则代替优先队列的出队操作
            the_min = 0
            the_index = 0
            j = 0
            for i in range(1, len(gvlist)):
                if (gvlist[i].know is True):
                    continue
                else:
                    if (j == 0):
                        the_min = gvlist[i].dist
                        the_index = i
                    else:
                        if (gvlist[i].dist < the_min):
                            the_min = gvlist[i].dist
                            the_index = i
                    j += 1
            # 此时已经找到了未知的最小的元素是谁
            gvset.remove(gvlist[the_index])  # 相当于执行出队操作
            return gvlist[the_index]

        # 逐渐遍历各个点，v为距离出发最小的那个路口
        v = get_unknown_min(mvlist, mvset)
        # print(v.vid,v.dist,v.outList)
        # 如果这个路口的know被标记为T，说明它已被计算过距出发点的最短路径
        v.know = True
        for w in v.outList:  # w为索引，每个路口的出边路口id
            if (mvlist[w].know is True):
                continue
            if (mvlist[w].dist == float('inf')):

                mvlist[w].dist = v.dist + edges[(v.vid, w)][0]
                # [0]为从路口v到路口w的道路的长度
                # [1]为这条道路的id
                mvlist[w].prev = v.vid
            else:
                if ((v.dist + edges[(v.vid, w)][0]) < mvlist[w].dist):
                    mvlist[w].dist = v.dist + edges[(v.vid, w)][0]
                    # mvlist[w].cross_rid.append(edges[(v.vid, w)][1])
                    mvlist[w].prev = v.vid
                else:  # 原路径长更小，没有必要更新
                    pass
    return mvlist