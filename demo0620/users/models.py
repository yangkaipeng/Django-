from django.db import models
from django.contrib.auth.models import User


# 创建用户模型，关联User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    org = models.CharField('组织', max_length=128, blank=True)
    telephone = models.CharField('联系方式', max_length=50, blank=True)
    mod_date = models.DateTimeField('最近更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user









