# -*- coding: utf-8 -*-
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils import timezone
from DjangoUeditor.models import UEditorField
# from fontawesome.fields import IconField


# Create your models here.
class CaseType(models.Model):
    name = models.CharField('案例类别名字', max_length=256)
    intro = models.TextField('案例类别简介', default='',blank=True)

    nav_display = models.BooleanField('导航显示', default=True)
    home_display = models.BooleanField('首页显示', default=True)

    def get_absolute_url(self):
        return reverse('column', args=(self.slug,))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '案例类别'
        verbose_name_plural = '案例类别'
        ordering = ['name']  # 按照哪个栏目排序

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(is_publish=True)

class Case(models.Model):
    title = models.CharField('标题', max_length=256)
    slug = models.SlugField('网址', max_length=256, unique=True)
    img = models.ImageField('展示图片', upload_to='pictures/case/%Y/%m/%d')
    abstract = models.TextField('摘要', max_length=54, blank=True, null=True,
                                help_text="可选项，最多54个字符")


    type = models.ForeignKey(CaseType, on_delete=models.CASCADE, verbose_name='案例类别')
    views = models.PositiveIntegerField('浏览量', default=0)

    # slug = models.CharField('网址', max_length=256, unique=True,blank=True)


    # author = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者')
    content = UEditorField('内容', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')

    is_hot = models.BooleanField('热门', default=False)
    is_publish = models.BooleanField('正式发布', default=True)
    pub_date = models.DateTimeField('发表时间',default = timezone.now)
    # pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    # update_time = models.DateTimeField('更新时间',default = timezone.now)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    objects = models.Manager()
    published = PublishedManager()


    def get_absolute_url(self):
        return reverse('app:case_detail', args=(self.slug,))
        # return reverse('app:case_detail', kwargs={'case_slug': self.slug})
    get_absolute_url.short_description = '绝对路径'

    # def save(self, *args, **kwargs):
    #     self.abstract = self.content[:254]
    #     # self.slug = 'case_{0}'.format(self.pk)
    #     super(Case, self).save(*args, **kwargs)

    def next_case(self):
        # 下一篇
        return Case.objects.filter(id__gt=self.id, is_publish=True).order_by('id').first()

    def prev_case(self):
        # 前一篇
        return Case.objects.filter(id__lt=self.id, is_publish=True).order_by('id').last()


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '案例'
        verbose_name_plural = '案例'

class CustomerType(models.Model):
    name = models.CharField('客户类别名字', max_length=256)
    # slug = models.CharField('客户类别网址', max_length=256, db_index=True)
    intro = models.TextField('客户类别简介', default='', blank=True)

    nav_display = models.BooleanField('导航显示', default=True)
    home_display = models.BooleanField('首页显示', default=True)

    # def get_absolute_url(self):
    #     return reverse('column', args=(self.slug,))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '客户类别'
        verbose_name_plural = '客户类别'
        ordering = ['name']  # 按照哪个栏目排序

# class Customer(models.Model):
#     # on_delete 当指向的表被删除时，将该项设为空
#     type = models.ForeignKey(CustomerType, verbose_name='案例类别')
#     title = models.CharField('标题', max_length=256)
#     img = models.ImageField('展示图片', upload_to='pictures/customer/%Y/%m/%d')
#     slug = models.CharField('网址', max_length=256, unique=True)
#
#     # author = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者')
#     content = UEditorField('内容', height=300, width=1000,
#                            default=u'', blank=True, imagePath="uploads/images/",
#                            toolbars='besttome', filePath='uploads/files/')
#
#     views = models.PositiveIntegerField('浏览量', default=0)
#
#     is_publish = models.BooleanField('正式发布', default=True)
#     pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
#     update_time = models.DateTimeField('更新时间', auto_now=True, null=True)
#
#     objects = models.Manager()
#     published = PublishedManager()
#
#     def get_absolute_url(self):
#         return reverse('app:customer_detail', args=(self.slug,))
#
#     def next_customer(self):
#         # 下一篇
#         return Customer.objects.filter(id__gt=self.id, is_publish=True).order_by('id').first()
#
#     def prev_customer(self):
#         # 前一篇
#         return Customer.objects.filter(id__lt=self.id, is_publish=True).order_by('id').last()
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name = '客户'
#         verbose_name_plural = '客户'

class Customer(models.Model):
    # on_delete 当指向的表被删除时，将该项设为空
    type = models.ForeignKey(CustomerType, on_delete= None, verbose_name='案例类别')
    title = models.CharField('标题', max_length=256)
    img = models.ImageField('展示图片', upload_to='pictures/customer/%Y/%m/%d')
    slug = models.CharField('网址', max_length=256, unique=True)

    # author = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者')
    content = UEditorField('内容', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')

    views = models.PositiveIntegerField('浏览量', default=0)

    is_publish = models.BooleanField('正式发布', default=True)
    pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('app:customer_detail', args=(self.slug,))

    def next_customer(self):
        # 下一篇
        return Customer.objects.filter(id__gt=self.id, is_publish=True).order_by('id').first()

    def prev_customer(self):
        # 前一篇
        return Customer.objects.filter(id__lt=self.id, is_publish=True).order_by('id').last()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = '客户'

class About(models.Model):
    name = models.CharField('模块名字', max_length=256)
    img = models.CharField('模块图标', max_length=256)
    title = models.CharField('标题', max_length=15)
    subtitle = models.CharField('副标题', max_length=256, blank=True,help_text='可选')
    # img = models.ImageField('图标', upload_to='pictures/about/%Y/%m/%d')
    content = UEditorField('内容', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')
    is_show = models.BooleanField('正式发布', default=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '关于公司'
        verbose_name_plural = verbose_name

class SettingsGroup(models.Model):
    name = models.CharField('分组名', max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '配置分组'
        verbose_name_plural = verbose_name



class Settings(models.Model):
    title = models.CharField('变量标题', max_length=256)
    value = models.CharField('变量值', max_length=256, blank=True)
    var = models.CharField('变量名', max_length=256)
    settingsgroup = models.ForeignKey(SettingsGroup, on_delete=None, verbose_name='分组')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name

class Banner(models.Model):
    '''
    轮播
    '''
    MENU_TPYE = (
        (1, '首页'),
        (2, '技术服务'),
        (3, '行业客户'),
        (4, '成功案例'),
        (5, '升级日志'),
        (6, '关于软诚'),
    )

    menu=models.IntegerField(choices=MENU_TPYE,verbose_name='菜单')
    image=models.ImageField(upload_to='banner',verbose_name='轮播图片')
    index=models.IntegerField(default=0,verbose_name='轮播顺序')
    desc1= models.CharField(default='', max_length=15, verbose_name='描述1',blank=True, help_text='可选项，最多15个字符')
    desc2 = models.CharField(default='', max_length=20, verbose_name='描述2',blank=True, help_text='可选项，建议不超过20个字符')
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')
    is_use = models.BooleanField('在用？', default=True)

    class Meta:
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.menu


class Notification(models.Model):
    """一个简化过的Notification类，拥有三个字段：

    - `user_id`: 消息所有人的用户ID
    - `has_readed`: 表示消息是否已读
    """
    title = models.CharField(verbose_name='标题',max_length=256)
    content = UEditorField('内容', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')
    # user_id = models.IntegerField(db_index=True)
    post_time = models.DateTimeField(verbose_name='发送时间')

    class Meta:
        verbose_name = '系统公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title