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
