import json
from rest_framework.response import Response
from rest_framework.decorators import api_view



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