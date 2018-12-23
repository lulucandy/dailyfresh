from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django_redis import get_redis_connection
from django.contrib.auth import authenticate

from goods.models import Goods_SKU

class CartAddView(View):
    def post(self,request):
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res':0,'errmsg':'请登录'})
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        #校验数据完整性
        if not all([sku_id,count]):
            return JsonResponse({'res':1,'errmsg':'数据不完整'})
        
        #校验添加商品数量
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'res':2,'errmsg':'商品数目出错'})
        
        #校验商品是否存在
        try:
            sku = Goods_SKU.objects.get(id = sku_id)
        except Goods_SKU.DoesNotExist:
            return JsonResponse({'res':3,'errmsg':'商品不存在或已下架'})
        
        #添加购物车记录
        conn = get_redis_connection('defalut')
        cart_key = 'cart_%d'%user.id
        
        #hget cart_key 属性
        cart_count = conn.hget(cart_key,sku_id)
        if cart_count:
            count = int(cart_count) + count
        
        #校验商品库存
        if count>sku.stock:
            return JsonResponse({'res':4,'errmsg':'商品库存不足'})
        
        #设置sku_id对应值 hset
        conn.hset(cart_key,sku_id,count)
        return JsonResponse({'res':5,'errmsg':'添加成功'})



