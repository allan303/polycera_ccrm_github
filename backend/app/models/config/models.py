from mongoengine import (
    StringField, EmailField, FloatField, IntField, ListField
)
from typing import List, Optional, Dict
# app
from app.models.base_model import BaseDocumentNoAttr
from .schemas import ConfigPD


class ValidateCode(BaseDocumentNoAttr):
    '''
    Summary: 储存email注册码
    '''
    email = EmailField()
    vcode = StringField()


def create_default_config():
    return {
        'location': ['安徽', '北京', '福建', '甘肃', '广东', '广西', '贵州', '海南', '河北', '河南', '黑龙江', '湖北', '湖南',
                     '吉林', '江苏', '江西', '辽宁', '内蒙古', '宁夏', '青海', '山东', '山西', '陕西', '上海', '四川', '天津',
                     '西藏', '新疆', '云南', '浙江', '重庆', '香港', '澳门', '台湾', '其他国内', '亚洲区域', '欧洲区域',
                     '韩国', '日本', '印度', '俄罗斯', '其他'],
        'source': ['展会', '交流会', '客户拜访', '网络或电话咨询', '老客户', '其他'],
        'industry': ['油气田', '电力', '重金属', '半导体', '光伏面板',
                     '化工', '垃圾', '印染', '医药', '特种分离', '市政', '其他'],
        'pjtype': ['新建或扩建', '技改', '换膜'],
        'wwtype': ['地下水',
                   '自来水',
                   '矿井水',
                   '地表水',
                   '市政中水',
                   '海水',
                   '循环排污水',
                   '冷凝液',
                   '高盐水',
                   '反渗透浓水',
                   '工业废水',
                   '油田采出水',
                   '压裂返排液',
                   '炼化含油废水',
                   '其他'
                   ],
        'pjstage': [
            {'name': '线索', 'win_percentage': 10},
            {'name': '方案及报价', 'win_percentage': 25},
            {'name': '已投标', 'win_percentage': 50},
            {'name': '指定我司', 'win_percentage': 75},
            {'name': '拟签合同', 'win_percentage': 90},
            {'name': '获得订单', 'win_percentage': 100},
            {'name': '丢失-竞争对手中标', 'win_percentage': 0},
            {'name': '丢失-项目取消', 'win_percentage': 0}
        ],
        'oemtype': ['业主', '代理商', '工程公司', '总包', '设计院', '经销商', '其他'],
        'department': ['设计及技术', '销售及商务', '采购', '运营', '管理层', '其他'],
        'title': ['总经理', '副总级别', '主管级别', '专工级别', '普通级别', '其他'],
        'product_units': ['支', '个', '套', 'pcs', 'set', '片', '组', '-'],
        'order_status': ['未签订', '已签订', '已收预付款', '已收全款', '已发货'],
        'chem': [
            {'text': '盐酸HCl', 'value': 'hcl'},
            {'text': '氢氧化钠NaOH', 'value': 'naoh'},
            {'text': '硫酸H2SO4', 'value': 'h2so4'},
            {'text': '柠檬酸Citric', 'value': 'citric'},
            {'text': '次氯酸钠NaClO', 'value': 'naclo'},
            {'text': 'EDTA螯合剂', 'value': 'edta'},
            {'text': '十二烷基苯磺酸钠SDBS', 'value': 'sdbs'},
            {'text': '聚铁PAC(Fe)', 'value': 'pac'},
            {'text': '聚铝PAC(Al)', 'value': 'pac(al)'},
        ],
    }


# class WwtpyEmbedded(EmbeddedDocument):
#     name = StringField()
#     flux_min = FloatField()
#     flux_max = FloatField()


# class PjstageEmbedded(EmbeddedDocument):
#     name = StringField()
#     win_percentage = IntField()

# class OemtypeOrm(BaseDocumentNoAttr):
#     name = StringField()
# class TitleOrm(BaseDocumentNoAttr):
#     name=StringField()
# class DepartmentOrm(BaseDocumentNoAttr):
#     name=StringField()
# class PjstageOrm(BaseDocumentNoAttr):
#     name = StringField()
#     win_percentage=StringField()
# class WwtypeOrm(BaseDocumentNoAttr):
#     name = StringField()
#     flux_min=FloatField()
#     flux_max =FloatField()


class ConfigOrm(BaseDocumentNoAttr):
    '''
    Summary: 所有 config 
    '''
    _classname = 'config'
    _children = ''  # 将会关联到此class的类
    _father = ''  # 此类关联的class

    location = ListField(StringField())
    source = ListField(StringField())
    industry = ListField(StringField())
    pjtype = ListField(StringField())
    # wwtype = EmbeddedDocumentListField(WwtpyEmbedded)
    # pjstage = EmbeddedDocumentListField(PjstageEmbedded)
    wwtype = ListField()
    pjstage = ListField()
    oemtype = ListField(StringField())
    department = ListField(StringField())
    title = ListField(StringField())
    product_units = ListField(StringField())
    order_status = ListField(StringField())
    chem = ListField()

    @classmethod
    def init_model(cls):
        dt = create_default_config()
        cls.objects.delete()
        cls(**dt).save()

    @property
    def pd(self) -> ConfigPD:
        return ConfigPD.from_orm(self)

    @classmethod
    def get_cache(cls) -> List[Dict]:
        '''
        Summary: Config 比较特殊
        NOTE： 手动缓存 改善性能
        '''
        obj = cls.objects.first()
        dt = obj.pd.dict()
        return dt
