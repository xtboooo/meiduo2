from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django.contrib.auth import login
from django.http import JsonResponse
from django.views import View
from oauth.models import OAuthQQUser
from oauth.utlis import generate_secret_openid
import logging

logger = logging.getLogger('django')


# GET /qq/authorization/?next=<登录之后的访问地址>
class QQLoginView(View):
    def get(self, request):
        """ 获取QQ登陆网址 """
        next1 = request.GET.get('next', '/')

        # 创建OAuthQQ对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next1)

        # 获取QQ登陆网址并返回
        login_url = oauth.get_qq_url()
        return JsonResponse({'code': 0,
                             'message': 'OK',
                             'login_url': login_url})


# GET /qq/oauth_callback/?code=<QQ返回的Authorization Code>
class QQUserView(View):
    def get(self, request):
        """ 获取QQ登录用户的openid并进行处理 """
        # 1.获取code
        code = request.GET.get('code')

        # 2.获取QQ登陆用户的openid
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, )

        try:
            # 根据code获取access_token
            access_token = oauth.get_access_token(code)

            # 根据access_token获取openid
            openid = oauth.get_open_id(access_token)

        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400,
                                 'message': 'QQ登陆失败'})

        # 3.根据openid是否已经和本网站用户进行绑定进行处理
        try:
            qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果未进行绑定, 将openid加密并进行返回
            secret_openid = generate_secret_openid(openid)
            return JsonResponse({'code': 300,
                                 'message': 'OK',
                                 'secret_openid': secret_openid}, )
        else:
            # 如果已经绑定,保存用户的登陆状态信息
            user = qq_user.user
            login(request, user)

            response = JsonResponse({'code': 0,
                                     'message': 'OK', })

            # 设置cookie
            response.set_cookie('username',
                                user.username,
                                max_age=14 * 24 * 3600,)

            return response
