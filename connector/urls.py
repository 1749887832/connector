"""connector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from port.jky.oltp import user_login as user
from port.jky.views.system_model import server_model as server
from port.jky.views.system_model import global_model as system_global

urlpatterns = [
    path('admin/', admin.site.urls),
    # 登录接口
    path('login/', user.User_Handle.User_Login),
    # 退出接口
    path('logout/', user.User_Handle.User_Logout),
    # 服务列表
    path('all-server/', server.Server_handle.show_server),
    # 修改服务状态
    path('update-server/', server.Server_handle.update_server),
    # 添加服务
    path('add-server/', server.Server_handle.add_server),
    # 删除服务
    path('delete-server/',server.Server_handle.delete_server),
    # 编辑服务
    path('editserver/', server.Server_handle.edit_server),
    # 获取系统变量
    path('show-global/',system_global.Global_handle.show_global)
]
