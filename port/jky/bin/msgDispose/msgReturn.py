import datetime


class Msg:
    def __init__(self):
        super().__init__()

    @classmethod
    def Success(cls, code=0, data=None, total=None, extend=None, msg='成功'):
        if extend is None:
            record = {
                'code': code,
                'data': data,
                'total': total,
                'msg': msg,
            }
        else:
            record = {
                'code': code,
                'data': {
                    'list': data,
                    'extend': extend
                },
                'total': total,
                'msg': msg,
            }
        return record

    @classmethod
    def Error(cls, code=-1, msg='网络错误'):
        record = {
            'code': code,
            'msg': msg,
        }
        return record


# 获取当前时间
class ReturnTime:
    def __init__(self):
        super().__init__()

    @staticmethod
    def getNowTime():
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now_time


# 判断是否全部为空
class JudgeAllIsNull:
    def __init__(self):
        super().__init__()

    @staticmethod
    def checkAndReturn(*args):
        for i in args:
            if i not in [None, '', 'null']:
                continue
            else:
                return False
        return True
