from django.db.models import Max
from django.http import JsonResponse
from port.jky.bin.msgDispose import msgReturn, msgCheck
from port.models import Step, Assert, Part, UserProfile


class StepHandle:
    def __init__(self):
        super().__init__()
        self.POST = None

    @msgCheck.login_check
    def showStep(self):
        # 获取id
        test_step = msgCheck.Check_type(self)
        test_id = test_step.get('id')
        page = int(test_step.get('page'))
        limit = int(test_step.get('limit'))
        try:
            all_step = Step.objects.filter(test_id=test_id).order_by('step_order')
            count = len(all_step)
            showstep = all_step[limit * (page - 1):limit * page]
            data = list()
            for step in showstep:
                content = dict()
                content['id'] = step.id
                content['step_url'] = step.step_url
                content['request_type'] = step.request_type
                content['request_data'] = step.request_data
                content['get_global'] = step.get_global
                content['response_result'] = step.response_result
                content['useGlobal'] = [globalname.use_global for globalname in Part.objects.filter(step_id=step.id)]
                content['create_time'] = step.create_time.strftime('%Y-%m-%d')
                content['create_user'] = UserProfile.objects.get(user_id=step.create_user).user_name
                content['step_content'] = step.step_content
                content['result'] = step.result
                content['order'] = step.step_order
                data.append(content)
            return JsonResponse(msgReturn.Msg().Success(data=data, total=count), safe=False)
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False)

    @msgCheck.login_check
    def addStep(self):
        add_step = msgCheck.Check_type(self)
        # 获取接口地址
        step_url = add_step.get('step_url')
        # 获取接口请求方式
        step_type = add_step.get('step_type')
        # 获取请求body
        step_body = add_step.get('step_content')
        # 获取断言参数
        step_assert = add_step.get('assert_name')
        # 获取是否存储变量
        step_delivery = add_step.get('delivery')
        # 获取存储变量
        step_global = add_step.get('global_content')
        # 获取描述
        step_content = add_step.get('step_data')
        # 获取case_id
        case_id = add_step.get('case_id')
        # 获取请求头
        header_value = add_step.get('header_value')
        if msgReturn.JudgeAllIsNull.checkAndReturn(header_value, add_step, step_url, step_type, step_body):
            print(step_delivery, case_id, header_value)
            try:
                # 查询用例的最大执行顺序
                maxOrder = Step.objects.filter(test_id=case_id).aggregate(Max('step_order'))
                # 写入步骤
                step_object = Step.objects.create(
                    step_url=step_url,
                    request_type=step_type,
                    request_data=step_body,
                    get_global=step_delivery,
                    create_user=add_step.user_id,
                    step_content=step_content,
                    create_time=msgReturn.ReturnTime.getNowTime(),
                    step_order=(0 if maxOrder['step_order__max'] is None else maxOrder['step_order__max']) + 1,
                    test_id=case_id,
                    step_headers=header_value,
                )
                print(1)
                step_object.save()
                step_id = step_object.id
                # 写入断言参数
                for i in list(step_assert):
                    Assert.objects.create(
                        argument=i['name'],
                        assert_type=i['type'],
                        assert_expect=i['value'],
                        argument_type=i['argument_type'],
                        step_id=step_id
                    )
                # 写入获取参数
                if step_delivery:
                    for i in list(step_global):
                        print(i)
                        Part.objects.create(
                            use_global=i['global_name'],
                            argument=i['urlarument'],
                            partIndex=i['urlindex'],
                            step_id=step_id
                        )
                return JsonResponse(msgReturn.Msg().Success(), safe=False)

            except Exception as e:
                return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False)
        else:
            return JsonResponse(msgReturn.Msg().Error(msg='必填参数不能为空'), safe=False, json_dumps_params={'ensure_ascii': False})

    """
        author：liuhuangxin
        time:2021年1月23日13:56:40
    """

    @msgCheck.login_check
    def delStep(self):
        try:
            delstep = msgCheck.Check_type(self)
            step_id = delstep.get('id')
            if len(Assert.objects.filter(step_id=step_id)) > 0:
                Assert.objects.filter(step_id=step_id).delete()
            if len(Part.objects.filter(step_id=step_id)) > 0:
                Part.objects.filter(step_id=step_id).delete()
            Step.objects.filter(id=step_id).delete()
            return JsonResponse(msgReturn.Msg().Success(msg='删除成功'), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})

    @msgCheck.login_check
    def showAllStep(self):
        try:
            testID = msgCheck.Check_type(self).get('testID')
            allStep = Step.objects.filter(test_id=testID).order_by('step_order')
            data = list()
            for step in allStep:
                content = dict()
                content['id'] = step.id
                content['order'] = step.step_order
                content['type'] = step.request_type
                content['url'] = step.step_url
                content['responseData'] = {}
                content['content'] = step.step_content
                data.append(content)
            return JsonResponse(msgReturn.Msg().Success(data=data), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})
