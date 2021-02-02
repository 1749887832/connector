from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
Test_status = [
    ('0', '未执行'),
    ('1', '通过'),
    ('2', '失败')
]
User_sex = [
    ('0', '男'),
    ('1', '女')
]
"""
    这是用户表
"""


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    # 姓名
    user_name = models.CharField(max_length=62, null=True, verbose_name='用户名')
    # 性别
    user_sex = models.CharField(max_length=32, null=False, default=User_sex[0][1], verbose_name='性别')
    # 所属部门
    user_branch = models.CharField(max_length=64, null=True, verbose_name='所属部门')
    # 电话
    user_phone = models.CharField(max_length=64, null=True, verbose_name='电话')
    # 绑定User表的id
    user = models.OneToOneField(User, on_delete=models.CASCADE)


"""
    这是服务名表
"""


class Server(models.Model):
    id = models.AutoField(primary_key=True)
    # 名字
    server_name = models.CharField(max_length=64, null=True, verbose_name='环境名')
    # ip地址
    server_ip = models.CharField(max_length=128, null=False, verbose_name='环境IP')
    # 描述
    server_describe = models.CharField(max_length=128, null=True, verbose_name='描述')
    # 状态
    server_status = models.CharField(max_length=32, null=False, default='true', verbose_name='状态')
    # 创建人
    create_user = models.IntegerField(null=False, verbose_name='创建人')
    # 创建时间
    create_time = models.DateTimeField(null=True, verbose_name='创建时间')


"""
    这是系统变量名
"""


class Global(models.Model):
    id = models.AutoField(primary_key=True)
    # 名字
    globals_name = models.CharField(max_length=32, null=True, verbose_name='变量名')
    # 使用变量
    use_name = models.CharField(max_length=32, null=True, verbose_name='使用名')
    # 变量类型
    globals_type = models.CharField(max_length=32, null=False, verbose_name='变量类型')
    # 状态(1表示实时，0表示固定)
    use_type = models.CharField(max_length=32, null=False, verbose_name='类型')
    # 存储方法还是接口
    globals_fun = models.CharField(max_length=32, null=True, verbose_name='实时方法')
    # 引用参数变量
    cite_arguments = models.CharField(max_length=32, null=False, verbose_name='参数名')
    # 创建时间
    create_time = models.DateTimeField(null=True, verbose_name='创建时间')
    # 描述
    content = models.CharField(max_length=128, null=True, verbose_name='描述')
    # 创建人
    create_user = models.IntegerField(null=False, verbose_name='创建人')


"""
    全局的接口
"""


class GlobalPort(models.Model):
    id = models.AutoField(primary_key=True)
    # 接口url
    globals_url = models.CharField(max_length=32, null=False, verbose_name='接口地址')
    # 请求方式
    globals_type = models.CharField(max_length=32, null=False, verbose_name='请求方式')
    # 请求头
    globals_headers = models.IntegerField(null=False, verbose_name='请求头')
    # 请求body
    globals_body = models.TextField(null=True, verbose_name='请求参数')
    # 获取参数
    globals_argument = models.CharField(max_length=32, null=True, verbose_name='获取参数')
    # 获取的下标
    globals_index = models.IntegerField(null=True, verbose_name='下标')


"""
    这是测试用例
"""


class Test(models.Model):
    id = models.AutoField(primary_key=True)
    # 用例标题
    test_name = models.CharField(max_length=32, null=False, verbose_name='标题')
    # 用例描述
    test_content = models.CharField(max_length=128, null=True, verbose_name='描述')
    # 创建人
    create_user = models.IntegerField(null=False, verbose_name='创建人')
    # 创建时间
    create_time = models.DateTimeField(null=False, verbose_name='创建时间')
    # 执行人
    execute_user = models.IntegerField(null=True, verbose_name='执行人')
    # 最后一次执行时间
    end_time = models.DateTimeField(null=True, verbose_name='执行时间')
    # 用例状态(0-->未执行，1-->通过,2-->失败)
    test_statue = models.CharField(max_length=32, null=False, default=Test_status[0][0], choices=Test_status, verbose_name='用例状态')
    # 用例所属测试单
    test_single = models.IntegerField(null=True, verbose_name='所属测试单')
    # 用例所属模块
    test_model = models.CharField(max_length=32, null=True, verbose_name='所属模块')


"""
    这是用例步骤
"""


class Step(models.Model):
    id = models.AutoField(primary_key=True)
    # 接口地址
    step_url = models.CharField(max_length=128, null=False, verbose_name='接口地址')
    # 请求方式
    request_type = models.CharField(max_length=32, null=False, verbose_name='请求方式')
    # 请求参数
    request_data = models.TextField(null=False, verbose_name='请求参数')
    # 是否获取参数
    get_global = models.CharField(max_length=32, null=True, verbose_name='是否获取参数')
    # 创建人
    create_user = models.IntegerField(null=True, verbose_name='创建人')
    # 创建时间
    create_time = models.DateTimeField(null=False, verbose_name='创建时间')
    # 请求返回结果
    response_result = models.TextField(null=True, verbose_name='响应信息')
    # 步骤结果
    result = models.CharField(max_length=32, null=True, verbose_name='结果')
    # 绑定请求头
    step_headers = models.IntegerField(null=True, verbose_name='请求头')
    # 步骤描述
    step_content = models.CharField(max_length=128, null=True, verbose_name='步骤描述')
    # 绑定的用例id
    test_id = models.IntegerField(null=True, verbose_name='用例ID')


"""
    这是局部变量
"""


class Part(models.Model):
    id = models.AutoField(primary_key=True)
    # 使用的变量名
    use_global = models.CharField(max_length=32, null=True, verbose_name='变量名')
    # 获取的参数名
    argument = models.CharField(max_length=32, null=True, verbose_name='参数名')
    # 绑定步骤id
    step_id = models.IntegerField(null=True, verbose_name='步骤ID')


"""
    这是断言类型
"""


class Assert(models.Model):
    id = models.AutoField(primary_key=True)
    # 参数
    argument = models.CharField(max_length=64, null=False, verbose_name='断言参数')
    # 断言类型
    assert_type = models.CharField(max_length=64, null=False, verbose_name='断言类型')
    # 断言参数类型
    argument_type = models.CharField(max_length=32, null=False, verbose_name='参数类型')
    # 断言期望
    assert_expect = models.CharField(max_length=64, null=False, verbose_name='断言期望')
    # 接口ID
    step_id = models.IntegerField(null=False, verbose_name='步骤ID')


"""
    这是系统请求头
"""


class Headers(models.Model):
    id = models.AutoField(primary_key=True)
    # 请求名
    headers_name = models.CharField(max_length=64, null=False, verbose_name='请求名')
    # 请求体
    headers_body = models.TextField(null=False, verbose_name='请求体')
    # 请求描述
    headers_content = models.CharField(max_length=128, null=True, verbose_name='请求描述')
    # 创建人
    create_user = models.IntegerField(null=False, verbose_name='创建人')
    # 创建时间
    create_time = models.DateTimeField(null=False, verbose_name='创建时间')
