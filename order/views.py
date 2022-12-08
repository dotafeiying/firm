from django.http import JsonResponse
from django.shortcuts import render
from django.db import transaction
from .models import Goods, OrderInfo
from .forms import OrderInfoForm, OrderCreateForm

from datetime import datetime
import random

# Create your views here.
# def goods_detail(request):
#     pass

def test(request):
    return render(request, 'order/test.html', {'form': OrderCreateForm()})

# @transaction.atomic
def order_commit(request):
    goods_id = request.POST.get('goods_id')
    email = request.POST.get('email')
    pay_method = request.POST.get('pay_method')
    total_price = request.POST.get('total_price')
    total_count = request.POST.get('total_count')
    print(goods_id,email,total_price,pay_method,total_count)
    if not all([goods_id, email, pay_method, total_count, total_price]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
    try:
        goods = Goods.objects.get(id=goods_id)
    except Goods.DoesNotExist:
        return JsonResponse({'res': 2, 'errmsg': '无效商品'})

    # 校验支付方式

    if pay_method not in [value[0] for value in OrderInfo.PAY_METHOD_CHOICES]:
        return JsonResponse({'res': 3, 'errmsg': '支付方式非法'})
    order_no = 'M%s' % datetime.now().strftime('%Y%m%d%H%M%S')
    # 设置事务保存点
    # sid = transaction.savepoint()

    try:
        OrderInfo.objects.create(order_no=order_no, goods_id=goods_id, total_count=total_count, total_price=total_price,
                                 pay_method=pay_method, email=email)
    except Exception as e:
        return JsonResponse({'res': 4, 'errmsg': '下单失败'})

    return JsonResponse({'res': 0, 'message': '订单创建成功', 'data': order_no})


def goods_detail(request, goods_slug):
    print(goods_slug)
    context = {}
    goods = Goods.objects.get(id=goods_slug)
    context['goods'] = goods
    context['form'] = OrderCreateForm()
    return render(request, 'order/goods_detail.html', context)

def order_pay(request):
    pass


