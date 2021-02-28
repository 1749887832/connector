from django.urls import path
from port.jky.core.model.serverModel.serverModel import ServerHandle
from port.jky.core.model.headerModel.headersModel import HeadersHandle
from port.jky.core.model.globalModel.globalModel import GlobalHandle
from port.jky.core.model.globalModel.debugGlobal import GlobalDebug

urlpatterns = [
    # 服务列表
    path('server/query/', ServerHandle.showServer),
    # 修改服务状态
    path('server/update/', ServerHandle.updateServer),
    # 添加服务
    path('server/add/', ServerHandle.addServer),
    # 删除服务
    path('server/delete/', ServerHandle.deleteServer),
    # 编辑服务
    path('server/edit/', ServerHandle.editServer),

    # 添加请求头
    path('headers/add/', HeadersHandle.addHeaders),
    # 显示请求头
    path('headers/query/', HeadersHandle.showHeaders),

    # 获取系统变量
    path('global/query/', GlobalHandle.showGlobal),
    # 添加变量接口
    path('global/add/', GlobalHandle.addGlobal),
    # 删除变量
    path('global/delete/', GlobalHandle.deleteGlobal),
    # 调试接口
    path('global/debug/', GlobalDebug.debugGlobal),
]
