from django.contrib import admin
from .models import UserProfile, User


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    # 根据指定的日期相关的字段，为页面创建一个时间导航栏，可通过日期过滤对象
    date_hierarchy = 'mod_date'
    # admin提供了自定义功能函数actions的手段，可以批量对数据进行修改
    actions = ['default_org']

    """
        action必须携带三个参数：
        当前的ModelAdmin，
        request，
        被选择的对象（即QuerySet）
    """
    def default_org(self, request, queryset):
        org_value = queryset.values()[0]['org']
        if org_value is None:
            rows_updated = queryset.update(org='金庸新作')
            self.message_user(request, "%s个员工信息已经被更新"%rows_updated)
        else:
            self.message_user(request, "该员工此信息已存在")
    default_org.short_description = '隶属作品'

# 可以用装饰器的方法，也可以用这种方法，注册
# admin.site.register(UserProfile, UserAdmin)
