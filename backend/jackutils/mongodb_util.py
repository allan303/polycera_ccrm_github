
def paginate(queryset,
             per_page: int = 20,
             page: int = 1):
    '''
    Summary: 对 queryset 进行分页,
    Params:
        per_page: 每页数量
        page: 第几页
    '''
    if not per_page:
        return queryset
    if not page or page < 1:
        page = 1
    start = (page-1)*per_page  # 0
    end = start + per_page  # 30
    return queryset[start:end]  # 0-29
