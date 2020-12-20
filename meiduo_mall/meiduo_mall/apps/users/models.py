from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ 用户模型类 """
    # 增加 mobile 字段
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")

    # 增加记录邮箱是否激活,默认为False:未激活
    email_active = models.BooleanField(default=False,
                                       verbose_name='邮箱验证状态')

    class Meta:
        db_table = "tb_users"
        verbose_name = "用户"
