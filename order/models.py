from django.db import models


# Create your models here.

class Goods(models.Model):
    name = models.CharField(max_length=40, verbose_name='商品名称')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='售价')
    password = models.CharField(max_length=20, verbose_name='解压密码')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class OrderInfo(models.Model):
    PAY_METHOD_CHOICES = (
        ('1', '支付宝支付'),
        ('2', '微信支付')
    )

    # ORDER_STATUS_ENUM = {
    #     'UNPAID': 1,
    #     'UNSEND': 2,
    #     'FINISHED': 3,
    # }
    ORDER_STATUS_CHOICES = (
        ('1', '未支付'),
        ('2', '已支付'),
        ('3', '订单信息出现问题'),
        ('4', '已完成'),
    )

    order_no = models.CharField(max_length=30, primary_key=True, verbose_name="订单号")
    # school = models.CharField(max_length=40, verbose_name='学校')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    total_count = models.IntegerField(default=1, verbose_name='商品数量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总价')
    pay_method = models.CharField(choices=PAY_METHOD_CHOICES, max_length=5, default='1', verbose_name="支付方式")
    mobile = models.CharField(max_length=50, verbose_name='手机')
    email = models.CharField(max_length=50, verbose_name='邮箱')
    status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=5, default='1', verbose_name="订单状态")
    trade_no = models.CharField(max_length=128, default='', verbose_name='支付编号')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        db_table = "order"
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_no

    @staticmethod
    def create(order_id, school, platform, name, password, subject, total_amount):
        order = OrderInfo(
            order_id=order_id,
            school=school,
            platform=platform,
            name=name,
            password=password,
            subject=subject,
            total_amount=total_amount,
            pay_method='1',
            status='1',
        )
        order.save()

