from django.db import models
from django.utils import timezone

# Create your models here.
Test_status = [
    ('0', '未执行'),
    ('1', '通过'),
    ('2', '失败')
]


class Server(models.Model):
    id = models.AutoField(primary_key=True)
    # 名字
    server_name = models.CharField(max_length=64, null=True)
    # ip地址
    server_ip = models.CharField(max_length=128, null=False)
    # 描述
    server_describe = models.CharField(max_length=128, null=True)
    # 状态
    server_status = models.CharField(max_length=32, null=False, default='true')
    # 创建时间
    create_time = models.DateTimeField(null=True)


class Global(models.Model):
    id = models.AutoField(primary_key=True)
    # 名字
    globals_name = models.CharField(max_length=32, null=True)
    # 使用变量
    use_name = models.CharField(max_length=32, null=True)
    # 变量类型
    globals_type = models.CharField(max_length=32, null=False)
    # 类型(1表示实时，0表示固定)
    use_type = models.CharField(max_length=32, null=False)
    # 引用参数变量
    cite_arguments = models.CharField(max_length=32, null=False)
    # 创建时间
    create_time = models.DateTimeField(null=True)
    # 描述
    content = models.CharField(max_length=128, null=True)
    # 创建人
    create_user = models.IntegerField(null=False)


class Test(models.Model):
    id = models.AutoField(primary_key=True)
    # 用例标题
    test_name = models.CharField(max_length=32, null=False, verbose_name='标题')
    # 用例描述
    test_content = models.CharField(max_length=1024, null=True, verbose_name='描述')
    # 创建人
    create_user = models.IntegerField(null=False, verbose_name='创建人')
    # 创建时间
    create_time = models.DateTimeField(null=False, default=timezone.now(), verbose_name='创建时间')
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
