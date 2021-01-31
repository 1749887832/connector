import datetime


class Msg:
    def __init__(self):
        super().__init__()

    def Success(self, code=0, data=None, total=None, msg='成功'):
        record = {
            'code': code,
            'data': data,
            'total': total,
            'msg': msg,
        }
        return record

    def Error(self, code=-1, msg='网络错误'):
        record = {
            'code': code,
            'msg': msg,
        }
        return record

    def ReNone(self, message):
        if message is None:
            message = ''
        return message


class ReturnTime:
    def __init__(self):
        super().__init__()

    @staticmethod
    def getnowTime():
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now_time
