import json
from urllib.parse import urlsplit

from django.http import JsonResponse, HttpResponseRedirect,HttpResponse
from django.shortcuts import render,reverse,redirect
from django.template import loader
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import Http404
# from django.urls import reverse
from django.db import transaction
from .models import Goods, OrderInfo, Post
from .forms import OrderInfoForm, OrderCreateForm, PostForm
from alipay import AliPay

from datetime import datetime
from decimal import Decimal
import random
import logging

logger = logging.getLogger(__name__)

def test(request):
    logger.debug(request.get_full_path())
    logger.debug(request.get_host())
    logger.debug(request.get_raw_uri())
    logger.debug(request.scheme)
    logger.debug(request.path_info)
    logger.debug(request.get_port())
    http = urlsplit(request.build_absolute_uri(None)).scheme
    host = request.META['HTTP_HOST']
    print('http',http)
    print('host',host)
    return render(request, 'order/test.html', {'form': OrderCreateForm()})


# @transaction.atomic
def order_commit(request):
    goods_id = request.POST.get('goods_id')
    email = request.POST.get('email')
    pay_method = request.POST.get('pay_method')
    total_price = request.POST.get('total_price')
    total_count = request.POST.get('total_count')
    extend_risk_fee = '0.16'

    if not all([goods_id, email, pay_method, total_count, total_price]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

    try:
        goods = Goods.objects.get(id=goods_id)
    except Goods.DoesNotExist as e:
        logger.error('商品无效，goods_id= %s', goods_id)
        return JsonResponse({'res': 2, 'errmsg': '无效商品'})
    total_extend_risk_fee = Decimal(extend_risk_fee) * int(total_count)
    # total_price = Decimal(total_price) + total_extend_risk_fee
    total_price = int(total_count) * goods.price + total_extend_risk_fee
    # 校验支付方式

    if pay_method not in [value[0] for value in OrderInfo.PAY_METHOD_CHOICES]:
        return JsonResponse({'res': 3, 'errmsg': '支付方式非法'})
    pay_method_display = {v[0]: v[1] for v in OrderInfo.PAY_METHOD_CHOICES}.get(pay_method)
    order_no = 'M%s' % datetime.now().strftime('%Y%m%d%H%M%S')
    # 设置事务保存点
    # sid = transaction.savepoint()

    try:
        OrderInfo.objects.create(order_no=order_no, goods_id=goods_id, total_count=total_count, total_price=total_price,
                                 pay_method=pay_method, email=email)
    except Exception as e:
        logger.error("创建订单%s失败，message= %s", order_no, e)
        return JsonResponse({'res': 4, 'errmsg': '下单失败'})

    return JsonResponse({'res': 0, 'message': '订单创建成功','order_no':order_no, 'data': {'html': loader.render_to_string('order/order_confirm.html',
                                                                                                 {'order_no': order_no,
                                                                                                  'pay_method_display': pay_method_display,
                                                                                                  'goods_name': goods.name,
                                                                                                  'total_count': total_count,
                                                                                                  'total_price': total_price,
                                                                                                  'total_extend_risk_fee': total_extend_risk_fee})}})

def return_url(request):
    if request.method == 'GET':
        params = request.GET.dict()
        sign = params.pop('sign')
        order_no = request.GET.get('out_trade_no')
        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,  # 网站私钥文件路径
            alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False, True代表沙箱环境
        )
        success = alipay.verify(params, sign)  # 返回 True or False
        if success:
            return redirect(reverse('order_detail') + '?order_no=' + order_no)
            # return HttpResponse('支付成功')
        logger.error("支付通知验签失败，order_no= %s, params= %s", order_no, params)
        return HttpResponse('支付失败')


def goods_detail(request, goods_slug):
    context = {}
    goods = Goods.objects.get(id=goods_slug)
    context['goods'] = goods
    context['form'] = OrderCreateForm()
    return render(request, 'order/goods_detail.html', context)


def order_detail(request):
    order_no = request.GET.get('order_no')
    if order_no is None:
        context = {}
        context['order'] = None
        context['goods'] = None
        return render(request, 'order/order_detail.html', context)
    try:
        order = OrderInfo.objects.get(order_no=order_no)
    except OrderInfo.DoesNotExist:
        logger.error('订单无效，order_no= %s', order_no)
        return render(request, 'order/404.html')
        # raise Http404("OrderInfo does not exist")
    context = {}
    context['order'] = order
    context['goods'] = order.goods
    return render(request, 'order/order_detail.html', context)

def terms(request):
    if request.method == 'POST':
        return render(request, 'order/terms.html')

def order_pay(request):
    if request.method == 'POST':
        logger.debug(request.get_full_path())
        logger.debug(request.get_host())
        logger.debug(request.get_raw_uri())
        logger.debug(request.scheme)
        logger.debug(request.path_info)
        logger.debug(request.get_port())
        request_data = json.loads(request.body.decode('utf-8'))
        order_no = request_data.get('order_no')
        checked = request_data.get('checked', True)
        print('check:',checked)
        print(type(checked))

        if not all([order_no]):
            return JsonResponse({'res': 1, 'errmsg': '订单id为空'})
        if not checked:
            return JsonResponse({'res': 1, 'errmsg': '请勾选同意《用户协议》'})

        try:
            order = OrderInfo.objects.get(order_no=order_no, status='1')
        except OrderInfo.DoesNotExist:
            logger.error('订单无效，order_no= %s', order_no)
            return JsonResponse({'res': 2, 'errmsg': '无效订单id'})

        total_pay = order.total_price  # Decimal

        if order.pay_method == '2':
            return JsonResponse({'res': 3, 'errmsg': '微信支付接口未开通'})

        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,  # 网站私钥文件路径
            alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False, True代表沙箱环境
        )


        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_no,  # 订单id
            total_amount=str(total_pay),  # 订单的实付款
            subject='测试订单%s' % order_no,  # 订单标题
            return_url=settings.RETURN_URL,
            # return_url='http://127.0.0.1:5000' + reverse('return_url'),
            # notify_url='http://luxijie.asuscomm.com:5000' + reverse('notify_url')  # 可选, 不填则使用默认notify url
            # notify_url = f'{request.scheme}://{request.get_host()}' + reverse('notify_url')  # 可选, 不填则使用默认notify url
            notify_url=settings.NOTIFY_URL  # 可选, 不填则使用默认notify url

        )

        pay_url = settings.ALIPAY_URL + "?" + order_string
        return JsonResponse({'res': 0, 'pay_url': pay_url})

def order_check1(request):
    if request.method == 'POST':
        order_no = request.POST.get('order_no')

        # 参数校验
        if not all([order_no]):
            return JsonResponse({'res': 1, 'errmsg': '订单id为空'})

        # 校验订单信息
        try:
            order = OrderInfo.objects.get(order_no=order_no, status='1', pay_method='1')
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '无效订单id'})

        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,  # 网站私钥文件路径
            alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False, True代表沙箱环境
        )

        while True:
            response = alipay.api_alipay_trade_query(out_trade_no=order_no)

            # 获取网关返回码
            code = response.get('code')
            print('code:', code)
            print('time:', datetime.now())
            print('trade_status:', response.get('trade_status'))

            if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
                # 支付成功
                # 获取支付宝交易号
                trade_no = response.get('trade_no')
                # 更新订单状态，设置支付宝交易号
                order.status = '2'  # 已支付
                order.trade_no = trade_no
                order.save()

                # 返回应答
                return JsonResponse({'res': 0, 'message': '支付成功'})
            elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
                # code == '40004': 支付交易订单还未创建，用户登录支付宝后就会创建
                # 等待买家付款
                import time
                time.sleep(5)
                continue
            else:
                # 支付失败
                return JsonResponse({'res': 3, 'errmsg': '支付失败'})

def order_check(request):
    if request.method == 'POST':
        order_no = request.POST.get('order_no')

        # 参数校验
        if not all([order_no]):
            return JsonResponse({'res': 1, 'errmsg': '订单id为空'})

        # 校验订单信息
        try:
            order = OrderInfo.objects.get(order_no=order_no, pay_method='1')
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '无效订单id'})

        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,  # 网站私钥文件路径
            alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False, True代表沙箱环境
        )
        if order.trade_no:
            response = alipay.api_alipay_trade_query(out_trade_no=order_no, trade_no=order.trade_no)
        else:
            response = alipay.api_alipay_trade_query(out_trade_no=order_no)
        logger.info('轮询订单状态，order_no= %s, resp= %s', order_no, response)
        code = response.get('code')
        if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
            return JsonResponse({'res': 0, 'message': '支付成功'})
        elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
            return JsonResponse({'res': 3, 'message': '待支付'})
        elif code == '20000':  # {'code': '20000', 'msg': 'Service Currently Unavailable', 'sub_code': 'aop.ACQ.SYSTEM_ERROR', 'sub_msg': '系统异常', 'buyer_pay_amount': '0.00', 'invoice_amount': '0.00', 'point_amount': '0.00', 'receipt_amount': '0.00'}
            return JsonResponse({'res': 3, 'message': '服务暂不可用，稍后重试'})
        else:
            # 支付失败
            return JsonResponse({'res': 4, 'errmsg': '支付失败'})

def review_status(request):
    if request.method == 'POST':
        order_no = request.POST.get('order_no')
        print('order_no: ', order_no)

        # 参数校验
        if not all([order_no]):
            return JsonResponse({'res': 1, 'errmsg': '订单id为空'})

        # 校验订单信息
        try:
            order = OrderInfo.objects.get(order_no=order_no)
        except OrderInfo.DoesNotExist:
            logger.error('订单无效，order_no= %s', order_no)
            return JsonResponse({'res': 2, 'errmsg': '无效订单id'})

        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,  # 网站私钥文件路径
            alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False, True代表沙箱环境
        )
        status = order.status
        status_display = order.get_status_display()
        trade_no = order.trade_no
        is_update = False

        if trade_no:
            response = alipay.api_alipay_trade_query(out_trade_no=order_no, trade_no=trade_no)
        else:
            response = alipay.api_alipay_trade_query(out_trade_no=order_no)
        logger.info("支付宝订单查询接口, order_no= %s, resp= %s", order_no, response)
        code = response.get('code')
        if code == '10000':
            if response.get('trade_status') == 'TRADE_SUCCESS':
                if status != '2':
                    order.status = '2'
                    order.trade_no = response.get('trade_no')
                    order.save()
                    is_update = True
            elif response.get('trade_status') == 'WAIT_BUYER_PAY':
                if status != '1':
                    order.status = '1'
                    order.save()
                    is_update = True
            elif response.get('trade_status') == 'TRADE_CLOSED':
                response = alipay.api_alipay_trade_fastpay_refund_query(out_request_no=order_no, trade_no=trade_no, out_trade_no=order_no)
                logger.info("支付宝退款查询接口, order_no= %s, resp= %s", order_no, response)
                code = response.get('code')
                if code == '10000':
                    if response.get('refund_status') == 'REFUND_SUCCESS':
                        if status != '5':
                            order.status = '5'
                            order.save()
                            is_update = True
                else:
                    return JsonResponse({'res': 3, 'errmsg': '接口返回错误', 'resp': response})
            else:
                return JsonResponse({'res': 3, 'errmsg': '接口返回错误', 'resp': response})
        elif code == '20000':
            return JsonResponse({'res': 3, 'errmsg': '服务暂不可用，稍后重试'})
        elif code == '40004':
            if status != '1':
                order.status = '1'
                order.save()
                is_update = True
        else:
            return JsonResponse({'res': 3, 'errmsg': '接口返回错误','resp': response})

        if is_update:
            logger.info(f'订单{order_no}状态已由 {status_display} 更新为 {order.get_status_display()}')
            return JsonResponse({'res': 0, 'message': f'订单{order_no}状态已由 {status_display} 更新为 {order.get_status_display()}'})
        return JsonResponse({'res': 0, 'message': '订单不需要更新','resp': response})




def order_refund(request):
    order_no = request.POST.get('order_no')

    # 参数校验
    if not all([order_no]):
        return JsonResponse({'res': 1, 'errmsg': '订单id为空'})

    # 校验订单信息
    try:
        order = OrderInfo.objects.get(order_no=order_no, pay_method='1')
    except OrderInfo.DoesNotExist:
        logger.error('订单无效，order_no= %s', order_no)
        return JsonResponse({'res': 2, 'errmsg': '无效订单id'})
    if order.status != '2':
        return JsonResponse({'res': 2, 'errmsg': '无法退款，订单必须为已支付状态'})

    app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
    alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,  # 应用id
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,  # 网站私钥文件路径
        alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False, True代表沙箱环境
    )

    trade_no = order.trade_no
    response = alipay.api_alipay_trade_query(out_trade_no=order_no, trade_no=trade_no)
    logger.info("支付宝订单查询接口, order_no= %s, resp= %s", order_no, response)
    code = response.get('code')
    if code == '10000':
        if response.get('trade_status') == 'TRADE_SUCCESS':
            response = alipay.api_alipay_trade_refund(str(order.total_price), out_trade_no=order_no, trade_no=order.trade_no)
            logger.info("订单发起退款, order_no= %s, resp= %s", order_no, response)
            if response.get('code') == '10000':
                order.status = '5'
                order.save()
                logger.info('订单退款成功, order_no= %s', order_no)
                return JsonResponse({'res': 0, 'message': '退款成功'})
            else:
                logger.error('订单退款失败, order_no= %s, resp= %s', order_no, response)
                return JsonResponse({'res': 3, 'errmsg': '退款失败', 'resp': response})
        elif response.get('trade_status') == 'TRADE_CLOSED':
            response = alipay.api_alipay_trade_fastpay_refund_query(out_request_no=order_no, trade_no=trade_no, out_trade_no=order_no)
            logger.info("支付宝退款查询接口, order_no= %s, resp= %s", order_no, response)
            if response.get('code') == '10000' and response.get('refund_status') == 'REFUND_SUCCESS':
                logger.info('订单为已退款状态，不要重复提交，order_no= %s', order_no)
                return JsonResponse({'res': 2, 'errmsg': '订单为已退款状态，不要重复提交'})
    logger.error('订单%s退款失败, resp= %s', order_no, response)
    return JsonResponse({'res': 3, 'errmsg': '退款失败', 'resp': response})




@csrf_exempt
def notify_url(request):
    """支付宝支付结果通知回调"""
    if request.method == 'POST':
        logger.debug(request.get_full_path())
        logger.debug(request.get_host())
        logger.debug(request.get_raw_uri())
        logger.debug(request.scheme)
        logger.debug(request.path_info)
        logger.debug(request.get_port())
        # from urllib.parse import parse_qs
        #
        # body_str = request.body.decode('utf-8')
        # post_data = parse_qs(body_str)
        #
        # post_dict = {}
        # for k, v in post_data.items():
        #     post_dict[k] = v[0]
        data = request.POST.dict()
        order_no = data.get("out_trade_no")

        # sign 不能参与签名验证
        signature = data.pop("sign")

        # 支付状态验证
        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,  # 网站私钥文件路径
            alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False, True代表沙箱环境
        )
        success = alipay.verify(data, signature)
        if not success:
            logger.error('验签失败, order_no= %s, request= %s', order_no, data)
            return HttpResponse('failure')

        # 3.查询订单支付信息: 订单编号, 支付金额
        try:
            order = OrderInfo.objects.get(order_no=order_no)
        except OrderInfo.DoesNotExist:
            logger.error('订单无效，order_no= %s', data.get("out_trade_no"))
            return HttpResponse('success')

        total_amount = data.get('total_amount')
        trade_no = data.get('trade_no')
        to_email = order.email
        if total_amount == str(order.total_price):
            if data["trade_status"] == "TRADE_SUCCESS":
                order.status = '2'
                order.trade_no = trade_no
                order.save()
                logger.info('订单支付成功, order_no= %s', order_no)

                subject = '路希捷网络商城卡密'
                message = ''
                sender = settings.EMAIL_FROM
                receiver = [to_email]
                html_message = """
                                        <h1>感谢您订购商品(%s)</h1>
                                        <p>解压密码为：%s</p>
                                        请点击以下链接查看订单详情<br/>
                                        <a href="http://127.0.0.1:5000/order/order_detail?order_no=%s">http://127.0.0.1:5000/order/order_detail?order_no=%s</a>
                                    """ % (order.goods.name, order.goods.password, order_no, order_no)
                try:
                    send_mail(subject, message, sender, receiver, html_message=html_message)
                    logger.info('邮件发送成功, order_no= %s', order_no)
                except Exception as e:
                    logger.error('发送邮件失败, order_no= %s'%order_no, exc_info=True)
            elif data["trade_status"] == "TRADE_FINISHED":
                order.status = '4'
                order.trade_no = trade_no
                order.save()
                logger.info('订单完成, order_no= %s', order_no)
            else:
                logger.error('订单尚未支付, order_no= %s', order_no)
        else:
            logger.error('订单金额不对, order_no= %s', order_no)
        return HttpResponse('success')


        # if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        #     # TODO 请在这里加上商户的业务逻辑程序代码 异步通知可能出现订单重复通知 需要做去重处理
        #     trade_no = data.get('trade_no')
        #     order.status = '2'
        #     order.trade_no = trade_no
        #     order.save()
        #     print("支付成功！")
        # else:
        #     print("尚未支付！")
        # return HttpResponse('success')

def post_detail(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            # order_no = form.cleaned_data['order_no']
            # reason = form.cleaned_data['reason']
            # email = form.cleaned_data['email']
            # alipay_no = form.cleaned_data['alipay_no']
            # content = form.cleaned_data['content']
            # Post.objects.create(order_no= order_no, reason=reason,email=email, alipay_no=alipay_no, content=content)
            messages.success(request, '您的投诉已经收到，我们将在24h回复您！')
            return redirect(reverse('post_detail'))
    else:
        form = PostForm()
    return render(request, 'order/post.html', {'form': form})