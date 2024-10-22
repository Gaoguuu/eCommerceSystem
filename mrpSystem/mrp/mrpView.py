import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
import datetime
import math
from queue import LifoQueue
import heapq


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
        if opera_type == "get_info":  # 获取问卷信息
            response = getInfo(info, request)
        else:
            response["code"] = "-7"
            response["msg"] = "请求类型有误"
    else:
        response["code"] = "-3"
        response["msg"] = "确少必要参数"

    return Response(json.dumps(response))


class TreeNode:
    def __init__(self, name, pro, number, predate, comdate):
        self.name = name
        self.pro = pro
        self.number = number
        self.predate = predate
        self.comdate = comdate
        self.chilist = []


# def getQuery(arrayQuery):
#     global Tree_list


def CreateRoot(MatNeed):
    name = MatNeed.name
    pro = (Material.objects.filter(MatName=name).first()).MatPro
    number = MatNeed.number
    comdate = MatNeed.date
    zday = 0
    tday = 0
    if pro == "生产":
        zday = (Material.objects.filter(MatName=name).first()).MatPre
    else:
        tday = (ALLO.objects.filter(ChiName=name).first()).MatPre + (
            ALLO.objects.filter(ChiName=name).first()
        ).ShoPre
    pday = zday + tday
    # 完成日期
    b = datetime.datetime.strptime(MatNeed.date, "%Y-%m-%d")
    # 下达日期
    predate = datetime.datetime.strftime(
        (b - datetime.timedelta(days=pday)), "%Y-%m-%d"
    )
    root = TreeNode(name, pro, number, predate, comdate)
    return root


def DFS(Nod):
    Nod.chilist.clear()
    ChiM = ALLO.objects.filter(ParName=Nod.name)
    if len(ChiM) > 0:
        for i in range(0, len(ChiM)):
            name = ChiM[i].ChiName
            maLos = ((Material.objects.filter(MatName=name)).first()).MatLos
            num = math.ceil((ChiM[i].ConNum * Nod.number / (1 - maLos)))
            # num = ChiM[i].ConNum * Nod.number
            comday = Nod.predate
            pro = (Material.objects.filter(MatName=name).first()).MatPro
            zday = 0
            tday = 0
            if pro == "生产":
                zday = (Material.objects.filter(MatName=name).first()).MatPre
            else:
                tday = (ALLO.objects.filter(ChiName=name).first()).MatPre + (
                    ALLO.objects.filter(ChiName=name).first()
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


def CLStore():
    # 从 Store 表中过滤数据并按 'MatID' 排序
    obj = Store.objects.filter(Q(MatPre__gt=0) | Q(MatRem__gt=0)).order_by("MatID")
    # 初始化优先队列
    priority_queue = []
    for i in range(0, len(obj)):
        name = obj[i].MatName
        print(name)
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


def show(request):
    if request.method == "GET":
        global Tree_list
        Tree_list = []
        ERP_list = []
        for i in range(0, len(Need_list)):
            root = CreateRoot(Need_list[i])
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

                if len(Need.childlist) != 0:
                    for i in range(0, len(Need.childlist)):
                        q.put(Need.childlist[i])  # 将子节点加入队列

        # 排序 ERP_list，按 predete 属性排序
        ERP_list.sort(key=lambda TreeNode: TreeNode.predate)

        return render(
            request, "show.html", {"Need_list": Need_list, "ERP_list": ERP_list}
        )

    return redirect("http://127.0.0.1:8000/home/")
