from django.http import JsonResponse

from port.jky.Controller import msg_check, msg_return
from port.models import Step


class Step_handle:
    def __init__(self):
        super().__init__()

    @msg_check.login_check
    def show_step(self):
        # 获取id
        test_step = msg_check.Check_type(self)
        test_id = test_step.get('id')
        try:
            all_step = Step.objects.filter(test_id=test_id)
            count = len(all_step)
            data = list()
            for step in all_step:
                content = dict()
                content['id'] = step.id
                content['step_url'] = step.step_url
                content['request_type'] = step.request_type
                content['request_data'] = step.request_data
                content['get_global'] = step.get_global
                content['argument'] = step.argument
                content['response_result'] = step.response_result
                content['result'] = step.result
                data.append(content)
            return JsonResponse(msg_return.Msg().Success(data=data, total=count), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)
