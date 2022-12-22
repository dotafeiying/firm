# -*- coding: utf-8 -*-
import os,django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','firm.settings')
django.setup()
from django.test import TestCase


# Create your tests here.
from alipay import AliPay
from django.conf import settings
from datetime import datetime
from order.models import OrderInfo



# order_no = 'M20221209213245'
# order_no = 'M20221214222909'
order_no = 'M20221215205243'
order = OrderInfo.objects.get(order_no=order_no)

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

# response = alipay.api_alipay_trade_fastpay_refund_query(order_no, trade_no='2022121522001475460505933221', out_trade_no=order_no)
# response = alipay.api_alipay_trade_refund('12.16', out_trade_no=order_no,trade_no='2022121322001475460505932562')
response = alipay.api_alipay_trade_query(out_trade_no=order_no, trade_no=order.trade_no )
print('api_alipay_trade_query: ', response)
response = alipay.api_alipay_trade_fastpay_refund_query(order_no, trade_no=order.trade_no, out_trade_no=order_no)
print('api_alipay_trade_fastpay_refund_query: ', response)
# response = alipay.api_alipay_trade_refund(str(order.total_price), out_trade_no=order_no,trade_no=order.trade_no)
# print('response: ', response)
# response = alipay.api_alipay_trade_query(out_trade_no=order_no, trade_no=order.trade_no)
# print('api_alipay_trade_query: ', response)
# response = alipay.api_alipay_trade_fastpay_refund_query(order_no, trade_no=order.trade_no, out_trade_no=order_no)
# print('api_alipay_trade_fastpay_refund_query: ', response)

# 获取网关返回码
code = response.get('code')
print('code:', code)
print('time:', datetime.now())
print('trade_status:', response.get('trade_status'))

