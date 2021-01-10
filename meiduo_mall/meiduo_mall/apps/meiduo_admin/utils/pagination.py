from rest_framework.pagination import PageNumberPagination


class StandardResultPagination(PageNumberPagination):
    """ 自定义分页类 """
    # 指定分页默认页容量
    page_size = 5

    # 指定获取分页数据时指定`页容量`的参数名称
    page_size_query_param = 'pagesize'

    # 指定分页最大页容量
    max_page_size = 20
