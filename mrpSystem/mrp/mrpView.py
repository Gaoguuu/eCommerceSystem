import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
import datetime
import math
from queue import LifoQueue, Queue
import heapq
from django.db.models import Q


@api_view(["POST"])
def opera(request):
    response = {"code": 0, "msg": "success"}
    body = str(request.body, encoding="utf-8")
    try:
        info = json.loads(body)  # 解析json报文
    except:
        response["code"] = "-2"
        response["msg"] = "请求格式有误"
    opera_type = info.get("opera_type")  # 获取操作类型
    if opera_type:
        if opera_type == "get_question_list":
            # 获取问卷信息
            response = show(info, request)
        else:
            response["code"] = "-7"
            response["msg"] = "请求类型有误"
    else:
        response["code"] = "-3"
        response["msg"] = "确少必要参数"
    print(response)
    return Response(response)


# 定义树节点
class TreeNode:
    def __init__(self, name, pro, number, predate, comdate):
        self.name = name
        self.pro = pro
        self.number = number
        self.predate = predate
        self.comdate = comdate
        self.chilist = []

    # 将节点转换为字典形式
    def to_dict(self):
        return {
            "name": self.name,
            "pro": self.pro,
            "number": self.number,
            "predate": str(self.predate),  # 转换为字符串，避免 datetime 序列化问题
            "comdate": str(self.comdate),
            "childlist": [child.to_dict() for child in self.chilist],
        }


# def getQuery(arrayQuery):
#     global Tree_list


# 创建树根节点
def CreateRoot(MatNeed):
    name = MatNeed["matName"]
    pro = (Material.objects.filter(MatName=name).first()).MatPro
    number = MatNeed["matNumber"]
    comdate = MatNeed["data"]
    zday = 0
    tday = 0
    if pro == "生产":
        zday = (Material.objects.filter(MatName=name).first()).MatPre
    else:
        tday = (Allo.objects.filter(ChiName=name).first()).MatPre + (
            Allo.objects.filter(ChiName=name).first()
        ).ShoPre
    pday = zday + tday
    # 完成日期
    b = datetime.datetime.strptime(MatNeed["data"], "%Y-%m-%d")
    # 下达日期
    predate = datetime.datetime.strftime(
        (b - datetime.timedelta(days=pday)), "%Y-%m-%d"
    )
    root = TreeNode(name, pro, number, predate, comdate)
    return root


# 进行深度搜索
def DFS(Nod):
    Nod.chilist.clear()
    ChiM = Allo.objects.filter(ParName=Nod.name)
    if len(ChiM) > 0:
        for i in range(0, len(ChiM)):
            name = ChiM[i].ChiName
            maLos = ((Material.objects.filter(MatName=name)).first()).MatLos
            # print(f"Nod.number: {Nod.number}, type: {type(Nod.number)}")
            # print(f"maLos: {maLos}, type: {type(maLos)}")

            num = math.ceil((ChiM[i].ConnNum * Nod.number / (1 - maLos)))
            # num = ChiM[i].ConNum * Nod.number
            comday = Nod.predate
            # date_obj = datetime.strptime(comday, "%Y-%m-%d").date()
            pro = (Material.objects.filter(MatName=name).first()).MatPro
            zday = 0
            tday = 0
            if pro == "生产":
                zday = (Material.objects.filter(MatName=name).first()).MatPre
            else:
                tday = (Allo.objects.filter(ChiName=name).first()).MatPre + (
                    Allo.objects.filter(ChiName=name).first()
                ).ShoPre
            pday = zday + tday
            b = datetime.datetime.strptime(comday, "%Y-%m-%d")
            predate = datetime.datetime.strftime(
                (b - datetime.timedelta(days=pday)), "%Y-%m-%d"
            )
            Node = TreeNode(name, pro, num, predate, comday)
            Nod.chilist.append(Node)
            DFS(Node)
    return None


# def EnsureTree(name):
#     q = LifoQueue()
#     index_of_min = 0
#     date = datetime.date.today()
#     mindate = datetime.date.today()

#     for i in range(0, len(Tree_list)):
#         q.put(Tree_list[i])

#         while q.empty() != True:
#             node = q.get()

#             if node.name == name:
#                 date = node.predate

#                 # 更新最小日期
#                 if mindate.__ge__(date):
#                     mindate = date
#                     index_of_min = i

#             if len(node.chilist) != 0:
#                 for i in range(len(node.chilist) - 1, -1, -1):
#                     q.put(node.chilist[i])
#             # else:
#             #     continue

#     return index_of_min


# 查询并清空库存
def CLStore():
    # 从 Store 表中过滤数据并按 'MatID' 排序
    obj = Store.objects.filter(Q(MatPre__gt=0) | Q(MatRem__gt=0)).order_by("MatID")
    for i in range(0, len(obj)):
        # 初始化优先队列
        priority_queue = []
        name = obj[i].MatName
        p = LifoQueue()
        for j in range(0, len(Tree_list)):
            p.put(Tree_list[j])
            while not p.empty():
                node = p.get()
                if node.name == name:
                    heapq.heappush(priority_queue, (node.predate, node))
                if len(node.chilist) != 0:
                    for k in range(len(node.chilist) - 1, -1, -1):
                        p.put(node.chilist[k])
        # # 初始化树结构，确保索引存在
        # index = EnsureTree(name)
        # root = Tree_List[index]

        sremain = obj[i].MatRem + obj[i].MatPre  # 剩余数量

        # 开始遍历优先队列
        while priority_queue and sremain > 0:
            # 取出优先队列中的元素
            _, node = heapq.heappop(priority_queue)
            if node.number > sremain:
                node.number = node.number - sremain
                DFS(node)
                break
            else:
                sremain = sremain - node.number
                node.number = 0
                DFS(node)

                # 再次遍历树，直到队列为空
                # while not q.empty():
                #     n_node = q.get()
                #     if n_node.name == name:
                #         sremain = sremain - n_node.number
                #         n_node.number = 0
                #         DFS(n_node)
                # q.put(Tree_List[len(Tree_List) - index - 1])
                # continue

            # if len(node.childlist) != 0:
            #     for i in range(len(node.childlist) - 1, -1, -1):
            #         q.put(node.childlist[i])
            # else:
            #     continue
    return None


# 入口函数
def show(info, request):
    mrpList = info.get("mrpList")
    response = {"code": 0, "msg": "success"}
    data = {}
    if 1 == 1:
        global Tree_list
        Tree_list = []
        ERP_list = []
        for i in range(0, len(mrpList)):
            root = CreateRoot(mrpList[i])
            Tree_list.append(root)
            DFS(root)
        CLStore()  # 调用 CLStore 函数，处理树结构中的节点

        for i in range(0, len(Tree_list)):
            root = Tree_list[i]
            q = Queue()
            q.put(root)

            while not q.empty():
                Need = q.get()

                if Need.number != 0:
                    ERP_list.append(
                        Need
                    )  # 如果该节点的 number 不为0，添加到 ERP_list 中

                if len(Need.chilist) != 0:
                    for i in range(0, len(Need.chilist)):
                        q.put(Need.chilist[i])  # 将子节点加入队列

        # 排序 ERP_list，按 predete 属性排序
        ERP_list.sort(key=lambda TreeNode: TreeNode.predate)
        response["erpList"] = [node.to_dict() for node in ERP_list]
        response["total"] = len(response["erpList"])

    return response
