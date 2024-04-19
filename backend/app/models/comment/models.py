from mongoengine import StringField, ListField
# app
from app.models.user.models import BaseDocumentOwner


class CommentOrm(BaseDocumentOwner):
    '''
    Summary: 评论 还是以独立的 document 存在，便于管理
    '''
    _classname = 'comment'
    _children = ''  # 将会关联到此class的类
    _father = 'post'  # 此类关联的class

    post_sid = StringField(required=True)
    at_users_sid = ListField(StringField())  # @ 的用户，后期用于 消息提醒
    body = StringField(default='')
    quote_comment = StringField(default='')  # 引用的评论

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='owner_name,body', **kwargs)
