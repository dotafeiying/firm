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

class ModelTest(object):

    def __init__(self):
        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()
        self.alipay = AliPay(
            appid=settings.ALIPAY_APPID,  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,  # 网站私钥文件路径
            alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False, True代表沙箱环境
        )

    def test_alipay(self):
        order_no = 'M20221220093109'
        order = OrderInfo.objects.get(order_no=order_no)
        response = self.alipay.api_alipay_trade_query(out_trade_no=order_no, trade_no=order.trade_no)
        print('api_alipay_trade_query: ', response)
        response = self.alipay.api_alipay_trade_fastpay_refund_query(order_no, trade_no=order.trade_no, out_trade_no=order_no)
        print('api_alipay_trade_fastpay_refund_query: ', response)

    def test_model(self):
        order_no = 'M2022122009310'
        order = OrderInfo.objects.filter(order_no=order_no).first()
        print(type(order), order)

if __name__ == '__main__':
    model = ModelTest()
    # model.test_alipay()
    model.test_model()