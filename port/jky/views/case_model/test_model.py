from django.http import JsonResponse
from port.jky.Controller import msg_return, msg_check
from port.models import Test


class Test_handle:
    def __init__(self):
        super().__init__()
        self.user = None

    def add_Test(self):
        print(self)
        data = msg_check.Check_type(self)
        casename = data.get('casename')
        caseesc = data.get('caseesc')
        casemodel = data.get('casemodel')
        userid = self.user.id
        test = Test.objects.create(
            test_name=casename,
            test_model=casemodel,
            test_content=caseesc,
            create_user=userid
        )
        test.save()
        print(casename, caseesc, casemodel, userid)
        return JsonResponse(msg_return.Msg().Success(), safe=False)
