from django.urls import path
from port.jky.lib.login.userLogin import UserLoginAndLogout
from port.jky.lib.user.userModel import UserHandle

urlpatterns = [
    # 登录接口
    path('login/', UserLoginAndLogout.userLogin),
    # 退出接口
    path('logout/', UserLoginAndLogout.userLogout),
    # 显示所有用户
    path('user/query/', UserHandle.showUser),
]
