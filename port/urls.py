from django.urls import path
from port.jky.oltp import user_login as user
from port.jky.views.system_model import server_model as server
from port.jky.views.system_model import global_model as system_global
from port.jky.views.case_model import test_model as system_test
urlpatterns = [
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
    path('delete-server/', server.Server_handle.delete_server),
    # 编辑服务
    path('editserver/', server.Server_handle.edit_server),
    # 获取系统变量
    path('show-global/', system_global.Global_handle.show_global),



    # 添加用例标题
    path('add-case/',system_test.Test_handle.add_Test)
]