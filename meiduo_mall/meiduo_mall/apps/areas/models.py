from django.db import models


class Areas(models.Model):
    """ 地区模型类 """
    # 创建name字段,用户保存名称
    name = models.CharField(max_length=20,
                            verbose_name='地区名称')

    # 自关联字段
    # 第一个参数是 self：指自己和自己关联
    # on_delete=models.SET_NULL：如果父级地区被删除，下级地区的 parent_id 置为NULL
    parent = models.ForeignKey(to='self',
                               on_delete=models.SET_NULL,
                               related_name='subs',
                               null=True,
                               blank=True,
                               verbose_name='父级地区', )

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '地区'

    def __str__(self):
        return self.name
