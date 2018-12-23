from django.db import models
from tinymce.models import HTMLField
from db.base_model import BaseModel
#商品种类表

class GoodsType(BaseModel):
    name = models.CharField(max_length = 20,verbose_name = '种类名称')
    logo = models.CharField(max_length = 20, verbose_name= '标识')
    image = models.ImageField(upload_to = 'Type',verbose_name = '商品类型图片')

    class Meta:
        db_table = 'df_goods_type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

#商品表
class Goods_SKU(BaseModel): 
    status_choices=(
        (0,'下线'),
        (1,'上线'),
    )
    type = models.ForeignKey('GoodsType',verbose_name ='商品种类',on_delete=models.DO_NOTHING)
    goods = models.ForeignKey('Goods',verbose_name='SPU_ID',on_delete=models.DO_NOTHING)
    name = models.CharField(max_length = 20,verbose_name = '商品名称')
    desc = models.CharField(max_length = 256, verbose_name= '商品简介')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name = '商品名称')
    unite = models.CharField(max_length = 20, verbose_name= '商品单位')
    stock = models.IntegerField(default = 1,verbose_name='商品库存')
    sale = models.IntegerField(default = 0,verbose_name='商品销量')
    image= models.ImageField(upload_to = 'Goods',verbose_name = '商品图片')
    status = models.SmallIntegerField(default=1,choices=status_choices,verbose_name='商品状态')

    class Meta:
        db_table = 'df_goods_sku'
        verbose_name = '商品'
        verbose_name_plural = verbose_name
    def __str__(self):
        id = str(self.id)
        return id

#商品SPU表
class Goods(BaseModel):
    name = models.CharField(max_length = 20,verbose_name = '商品名称')
    detail = HTMLField(blank = True,verbose_name = '商品详情')

    class Meta:
        db_table = 'df_goods'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

#商品图片表
class Goodsimage(BaseModel):
    images = models.ImageField(upload_to ='Goods',verbose_name='商品图片')
    sku = models.ForeignKey('Goods_SKU',verbose_name = 'SKU_ID',on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'df_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.sku

#首页轮播商品表
class IndexGoodsBanner(BaseModel):
    sku = models.ForeignKey('Goods_SKU',verbose_name = 'SKU_ID',on_delete=models.DO_NOTHING)
    images = models.ImageField(upload_to ='banner',verbose_name='轮播图片')
    index = models.SmallIntegerField(default=0,verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '首页轮播商品表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.index)
    
#首页促销活动表
class IndexPromotionBanner(BaseModel):
    name = models.CharField(max_length = 20,verbose_name = '商品名称')
    # url = models.CharField(max_length = 256 verbose_name='活动链接')
    url = models.CharField(max_length = 256 ,verbose_name='活动链接')
    images = models.ImageField(upload_to ='banner',verbose_name='活动图片')
    index = models.SmallIntegerField(default=0,verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = '主页促销活动表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

#首页分类商品展示表
class IndexTypeGoodsBanner(BaseModel):
    DISPLAY_TYPE_CHOICES=(
        (0,'标题'),
        (1,'图片'),
    )


    sku = models.ForeignKey('Goods_SKU',verbose_name = 'SKU_ID',on_delete=models.DO_NOTHING)
    type = models.ForeignKey('GoodsType',verbose_name = '商品类型',on_delete=models.DO_NOTHING)
    index = models.SmallIntegerField(default=0,verbose_name='展示顺序')
    display_type = models.SmallIntegerField(default = 1,choices = DISPLAY_TYPE_CHOICES,verbose_name = '展示标识')

    class Meta:
        db_table = 'df_index_type_goods'
        verbose_name = "主页分类展示商品"
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.sku)