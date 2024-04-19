'''
手动缓存
'''
from typing import List
from app.models.post.models import PostOrm
from app.models.project.models import ProjectOrm, ProjectUpdateOrm, ProjectOemOrm
from app.models.oem.models import OemOrm
from app.models.contact.models import ContactOrm
from app.models.order.models import OrderOrm, OrderUpdateOrm
from app.models.pilot.models import PilotOrm
from app.models.product.models import ProductOrm
from app.models.user.models import UserOrm
from app.models.config.models import ConfigOrm
from app.models.design.models import DesignOrm
from app.models.role.models import RoleOrm
from app.models.design_module.models import DesignModuleOrm
from app.models.design.models import DesignOrm, StandardDesignOrm
from app.models.workgroup.models import WorkgroupOrm


def create_order_keywords_cache():
    dt = {}
    dt['post'] = PostOrm.order_keywords_dict()
    dt['user'] = UserOrm.order_keywords_dict()
    dt['project'] = ProjectOrm.order_keywords_dict()
    dt['project_oem'] = ProjectOemOrm.order_keywords_dict()
    dt['project_update'] = ProjectUpdateOrm.order_keywords_dict()
    dt['oem'] = OemOrm.order_keywords_dict()
    dt['contact'] = ContactOrm.order_keywords_dict()
    dt['order'] = OrderOrm.order_keywords_dict()
    dt['order_update'] = OrderUpdateOrm.order_keywords_dict()
    dt['pilot'] = PilotOrm.order_keywords_dict()
    dt['design'] = DesignOrm.order_keywords_dict()
    dt['role'] = RoleOrm.order_keywords_dict()
    dt['product'] = ProductOrm.order_keywords_dict()
    dt['design_module'] = DesignModuleOrm.order_keywords_dict()
    dt['design'] = DesignOrm.order_keywords_dict()
    dt['standard_design'] = StandardDesignOrm.order_keywords_dict()
    dt['workgroup'] = WorkgroupOrm.order_keywords_dict()
    return dt


def create_mycache():
    dt = {}
    dt['user'] = UserOrm.get_cache()
    dt['project'] = ProjectOrm.get_cache()
    dt['oem'] = OemOrm.get_cache()
    dt['contact'] = ContactOrm.get_cache()
    dt['order'] = OrderOrm.get_cache()
    dt['pilot'] = PilotOrm.get_cache()
    dt['role'] = RoleOrm.get_cache()
    dt['product'] = ProductOrm.get_cache()
    dt['config'] = ConfigOrm.get_cache()
    dt['design_module'] = DesignModuleOrm.get_cache()
    dt['design'] = DesignOrm.get_cache()
    dt['standard_design'] = StandardDesignOrm.get_cache()
    dt['order_keywords'] = create_order_keywords_cache()
    dt['workgroup'] = WorkgroupOrm.get_cache()
    return dt


def get_sid_name_cache(mycache: dict, sid_name: str) -> List:
    '''
    Summary: 根据sid_name(如 project_sid) 获取 mycache中的 key值
    project_sid --> project 
    owner_sid --> user
    NOTE:如果使用缓存，这应该是前台的事情，后台不需要考虑
    '''
    manual_dt = {
        'owner_sid': 'user'
    }
    if sid_name in manual_dt:
        return mycache[manual_dt[sid_name]]
    if sid_name.endswith('_sid'):
        return mycache[sid_name[:-4]]
    return []

