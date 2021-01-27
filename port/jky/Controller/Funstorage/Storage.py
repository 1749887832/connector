import datetime
import json


class All_Stoarage:
    def __init__(self):
        self.Get_now = self.Get_now()
        super().__init__()

    def Get_now(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        return now


data = '{"stime":${Get_now},"etime":"2021-01-27","reType":1,"payChannel":["THIRD_PARTY","CASH","BOC_POS_OLD","SMART_POS","WX_PAY","ALI_PAY",' \
       '"BOC_PUB","BOC_APP"],"schoolAreas":[2389]}'

if __name__ == '__main__':
    print(All_Stoarage().Get_now)
    for i, v in json.loads(data).items():
        if i == 'stime':
            print(getattr(All_Stoarage(), v))
        print(i, v)
