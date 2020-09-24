"""
0001 ~ 0200: 成功
0201 ~ 0400： 失败
"""

ANSWER_SAVE_SUCCESS = {
    "code": "0001",
    "success": True,
    "msg": "答题卡保存成功"
}

WJ_NOT_EXISTS = {
    "code": "0201",
    "success": False,
    "msg": "指定的问卷不存在"
}

ANSWER_PARA_ERROR = {
    "code": "0202",
    "success": False,
    "msg": "答题卡参数错误"
}

ANSWER_SAVE_ERROR = {
    "code": "0203",
    "success": False,
    "msg": "传入的字段不符合要求"
}