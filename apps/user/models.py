from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from db.base_model import BaseModel


class User(AbstractUser,BaseModel):
    #用户模型类
    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class AddressManager(models.Manager):
    def get_default_address(self,user):
        try:
            address =  self.get(user=user,is_default=True)
        except self.model.DoesNotExist:
            address = None
        return address


class Address(BaseModel):
    #地址模型类
    user = models.ForeignKey('User',verbose_name = '所属用户',on_delete=models.DO_NOTHING)
    receiver = models.CharField(max_length = 20 ,verbose_name = '收件人')
    addr = models.CharField(max_length = 256 , verbose_name = '收货地址' )
    zip_code = models.CharField(max_length = 5 ,null = False, verbose_name = '邮政编码' )
    phone = models.CharField(max_length = 11 , verbose_name = '联系电话' )
    is_default = models.BooleanField(default= False,verbose_name= '是否为默认地址')

    objects = AddressManager()
    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name
