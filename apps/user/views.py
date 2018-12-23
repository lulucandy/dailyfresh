from django.shortcuts import render,redirect
from django.views.generic import View
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from user.models import User,Address
from goods.models import Goods_SKU
from django.conf import settings
from django.http import HttpResponse
from django_redis import get_redis_connection 

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from utils.mixin import LoginRequiredMixin

import re
 
class RegisterView(View): 
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        #接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        #校验数据
        if not all([username,password,email]):
            return render(request,'register.html',{'errmsg':'数据不完整'})

        #校验邮箱
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request,'register.html',{'errmsg':'邮箱格式不正确'})

        if allow != 'on' :
            return render(request,'register.html',{'errmsg':'请同意协议'})
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        #注册
        user = User.objects.create_user(username,email,password)
        #默认是否激活为0
        user.is_active = 0
        user.save()
        #加密用户身份信息，生成激活cookie
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info)
        token = token.decode()
        #发送激活邮件（包含激活链接）
        subject = '天天生鲜欢迎信息'
        # href = 'http://127.0.0.1:8000/user/active/'%(token)
        # print(href)
        message = ''
        sender = settings.EMAIL_FROM
        receiver = [email]
        html_message = '尊敬的%s，欢迎您成为天天生鲜注册会员！请点击下面链接激活您的账户！<a href = "http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>'%(username, token, token)
        send_mail(subject,message,sender,receiver,html_message=html_message)
        #返回应答
        return redirect(reverse('goods:index'))

#用户激活 
class ActiveView(View):
    def get(self,request,token):
        #进行用户激活
        serializer = Serializer(settings.SECRET_KEY,3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']
            #根据Id修改数据库
            user = User.objects.get(id = user_id)
            user.is_active = 1
            user.save()
            #跳转到登录页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            #激活链接已过期
            return HttpResponse('激活链接已过期')
            #跳转到注册页面
            #return redirect(reverse('user:Register'))

class LoginView(View):
    '''登录'''
    def get(self, request):
        '''显示登录页面'''
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        # 使用模板
        return render(request, 'login.html', {'username':username, 'checked':checked})

    def post(self, request):
        '''登录校验'''
        # 接收数据
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        # if __debug__:
        #     import pdb
        #     pdb.set_trace()
        # 校验数据
        if not all([username, pwd]):
            return render(request, 'login.html', {'errmsg':'数据不完整'})
        try:
            # if __debug__:
            #     import pdb
            #     pdb.set_trace()
            user = User.objects.get(username = username)
            passwd = user.password

            if check_password(pwd,passwd):
                if user.is_active:
                    # 用户已激活
                    # 记录用户的登录状态
                    login(request,user)
                    # 获取登录后所要跳转到的地址
                    # 默认跳转到首页
                    next_url = request.GET.get('next', reverse('goods:index'))

                    # 跳转到next_url
                    response = redirect(next_url) # HttpResponseRedirect

                    # 判断是否需要记住用户名
                    remember = request.POST.get('remember')

                    if remember == 'on':
                        # 记住用户名
                        response.set_cookie('username', username, max_age=7*24*3600)
                    else:
                        response.delete_cookie('username')

                    # 返回response
                    return response
                else:
                    # 用户未激活
                    return render(request, 'login.html', {'errmsg':'账户未激活'})
            else:
                # 用户名或密码错误
                return render(request, 'login.html', {'errmsg':'用户名或密码错误'})

        except User.DoesNotExist:
            return render(request, 'login.html', {'errmsg':'用户名不存在'})

#用户中心信息页
class UserInfoView(LoginRequiredMixin, View):
    def get(self,request):
        user = request.user
        address = Address.objects.get_default_address(user)
        #获取用户地址信息
        #获取用户浏览记录
        # from redis import StrictRedis
        # StrictRedis(host='10.245.58.58',port='6379',db=3)
        #连接redis
        con = get_redis_connection('default')
        #取键值
        history_key = 'history_%d'%user.id
        #获取最近浏览的商品id
        sku_ids = con.lrange(history_key,0,4)
        #查数据库中商品具体信息
        goods_li=[]
        for id in sku_ids:
            goods = GoodsSKU.objects.grt(id = id)
            goods_li.append(goods)
        #组织上下文
        context = {'page':'user','address':address,'goods_li':goods_li}
        return render(request,'user_center_info.html',context)

#订单页
class UserOrderView(LoginRequiredMixin ,View):
    def get(self,request):
        return render(request,'user_center_order.html',{'page':'order'})

        #获取用户订单信息

#地址页
class AddressView(LoginRequiredMixin ,View):
    def get(self,request):
        #获取用户默认收货地址
        user = request.user
        address = Address.objects.get_default_address(user)
        return render(request,'user_center_site.html',{'page':'address','address':address }) 
    def post(self,request):
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        if not all([receiver,addr,zip_code,phone]):
            return render(request,'user_center_site.html',{'errmsg':'数据不完整'})
        if not re.match(r'1[3|4|5|7|8][0-9]{9}$',phone):
            return render(request,'user_center_site.html',{'errmsg':'手机号码格式不正确'})
        user = request.user
        address = Address.objects.get_default_address(user)
        
        if address:
            is_default = False
        else:
            is_default = True
        Address.objects.create(user=user,addr=addr,receiver=receiver,zip_code=zip_code,phone=phone,is_default=is_default)
        return redirect(reverse('user:address'))

#退出登录
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('goods:index'))