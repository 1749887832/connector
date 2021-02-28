import datetime


class AllStorages:
    def __init__(self):
        self.get_now = self.get_now()
        super().__init__()

    @classmethod
    def getNowTime(cls):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        return now_time
