from django.db import models


# Create your models here.

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
