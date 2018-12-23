from django.db import models
from db.base_model import BaseModel


class OrderInfo(BaseModel):
    PAY_METHOD_CHOICES=(
        (1,'货到付款'),
        (2,'微信支付'),
        (2,'支付宝支付'),
    )  
    ORDER_STATUS_CHOICES=(
        (1,'待支付'),
        (2,'待发货'),
        (3,'待评价'), 
        (4,'已评价'),
        (5,'已完成'),
    )

    order_id = models.CharField(max_length=128, verbose_name='支付编号')
    user = models.ForeignKey('user.User',on_delete=models.DO_NOTHING,verbose_name='用户ID')
    addr = models.ForeignKey('user.Address',on_delete=models.DO_NOTHING,verbose_name='用户地址')
    pay_method = models.SmallIntegerField(default=2,choices=PAY_METHOD_CHOICES,verbose_name='支付方式')
    total_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='总金额')
    total_count = models.IntegerField(default=1,verbose_name='总数量')
    transit_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='运费')
    order_status = models.SmallIntegerField(default=0,choices=ORDER_STATUS_CHOICES,verbose_name='订单状态')
    trade_no = models.CharField(max_length=128, verbose_name='支付编号')

    class Meta:
        db_table = 'df_order_info'
        verbose_name = '订单'
        verbose_name_plural = verbose_name

class OrderGoods(BaseModel):
    order = models.ForeignKey('OrderInfo', verbose_name='订单',on_delete=models.DO_NOTHING)
    sku = models.ForeignKey('goods.Goods_SKU', verbose_name='商品SKU',on_delete=models.DO_NOTHING)
    count = models.IntegerField(default=1, verbose_name='商品数目')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    comment = models.CharField(max_length=256, verbose_name='评论')

    class Meta:
        db_table = 'df_order_goods'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name