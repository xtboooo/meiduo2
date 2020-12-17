"""
xtbo97
"""
# 导入Celery对象
from celery_tasks.main import celery_app


# @celery_app.task(name='任务名称')
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """ 封装任务函数代码 """
    print('发送短信任务函数代码')
    print(f'手机号为:{mobile}  验证码为:{sms_code}')
