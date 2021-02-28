from django.urls import path

from port.jky.core.test.cellModel.cellModel import CellHandle
from port.jky.core.test.caseModel.caseModel import CaseHandle
from port.jky.core.test.caseModel.debugCase import CaseDebug
from port.jky.core.test.caseModel.stepModel.stepModel import StepHandle
from port.jky.core.test.caseModel.stepModel.debugStep import StepDebug
urlpatterns = [
    # 添加测试单
    path('cell/add/', CellHandle.addCell),

    # 显示所有用例
    path('case/query/', CaseHandle.showCase),
    # 添加用例标题
    path('case/add/', CaseHandle.addCase),

    # 调试所有的步骤
    path('case/debug/', CaseDebug.debugCase),

    # 添加用例步骤
    path('step/add/', StepHandle.addStep),
    # 删除用例步骤
    path('step/delete/', StepHandle.delStep),
    # 用例步骤的调试
    path('step/debug/', StepDebug.debugStep),
    # 显示所有的用例步骤
    path('step/query/', StepHandle.showStep),
    # 显示所有的步骤
    path('cases/query/', StepHandle.showAllStep),
]
