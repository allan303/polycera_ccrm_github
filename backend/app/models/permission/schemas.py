from typing import Optional, List
# appOrmModePD
from jackutils.dict_tool import dict_to_list

'''
Summary: role 和 权限
PermPD: 全部权限 --> List
Perm1PD: 单个模块权限，如Project --> Dict
Perm2PD: 权限类型，如 create --> Dict ,其中包括了 Scopes，即权限作用范围，如 edit--> self, team 可以编辑本人和团队的

权限作为一个dict存在，直接保存在role 或者 user 下的权限中
1） Role 和 User Permission结合：
    采用 or ，即只要其中之一为 True，则为True
'''


perm_models = {'post': '日志',
               'project': '项目',
               'oem': '客户',
               'contact': '联系人',
               'pilot': '实验',
               'comment': '评论',
               'product': '产品(订单库存)',
               'design_module': '产品(设计)',
               'design': '方案设计',
               'standard_design': '标准设计',
               'order': '订单',
               'quote': '报价',
               'auth': '个人',
               'wechat': '微信',
               'stock': '库存'}

perm_actions = {'create': '创建',
                'read': '查看',
                'edit': '编辑',
                'delete': '删除',
                # 'real_delete': '彻底删除',
                'assign': '分配',
                'download_one': '下载单个',
                'download_many': '下载多个',
                'clone': '克隆',
                'dashboard': '报表',
                'merge': '合并'}

perm_scopes = {'me': '本人', 'total': '全部'}

perm_option = {
    'models': dict_to_list(dt=perm_models, key_text='value', value_text='text'),
    'actions': dict_to_list(dt=perm_actions, key_text='value', value_text='text'),
    'scopes': dict_to_list(dt=perm_scopes, key_text='value', value_text='text')
}
