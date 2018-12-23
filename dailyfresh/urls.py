
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/',include('tinymce.urls')) ,                       #富文本编辑器
    path('user/', include('user.urls', namespace = 'user')),           #购物车模块
    path('cart/', include('cart.urls',namespace = 'cart')),           #商品模块
    path('order/',include( 'order.urls',namespace = 'order')),          #订单模块
    path('',include( 'goods.urls',namespace = 'goods' )),           #用户模块
]
