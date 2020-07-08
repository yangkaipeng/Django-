from django.utils.deprecation import MiddlewareMixin


# 自制中间件对权限进行控制
class AuthMD(MiddlewareMixin):
    urls = ['profile', 'logout']

    def process_request(self, request):
        from django.shortcuts import redirect
        # 获取域名
        urlinfo = request.path_info
        print(urlinfo)
        for url in self.urls:
            if url in urlinfo:
                # 验证是否处于登录状态
                if request.user.is_authenticated:
                    return
                else:
                    redirect('/users/login/')

