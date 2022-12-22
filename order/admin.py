from django.contrib import admin
from order.models import Goods, OrderInfo, Post
from django.conf import settings
from django.contrib import messages
from django.utils.html import format_html
from alipay import AliPay
import logging

logger = logging.getLogger(__name__)


# Register your models here.
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'email', 'total_count','total_price','pay_method','trade_no','create_time','update_time','color_status','review_status','order_refund']
    list_display_links = ('order_no',)
    search_fields = ['order_no']
    list_filter = ['status','pay_method']

    actions = ['make_refund', 'make_check_status']

    def make_check_status(self, request, queryset):
        verbose_name_plural = getattr(self.model._meta, 'verbose_name_plural', self.model._meta.model_name)
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
        update_list = []
        not_update_list = []
        failure_list = []
        order_num = queryset.count()

        for order in queryset:
            print('order:', order)
            order_no = order.order_no
            status = order.status
            status_display = order.get_status_display()
            trade_no = order.trade_no
            is_update = False

            try:
                if trade_no:
                    response = alipay.api_alipay_trade_query(out_trade_no=order_no, trade_no=trade_no)
                else:
                    response = alipay.api_alipay_trade_query(out_trade_no=order_no)
            except Exception as e:
                failure_list.append(f'订单{order_no}接口返回错误，{e}')
                continue
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
                    try:
                        response = alipay.api_alipay_trade_fastpay_refund_query(out_request_no=order_no, trade_no=trade_no,
                                                                                out_trade_no=order_no)
                        logger.info("支付宝退款查询接口, order_no= %s, resp= %s", order_no, response)
                    except Exception as e:
                        failure_list.append(f'订单{order_no}接口返回错误，{e}')
                        continue
                    code = response.get('code')
                    if code == '10000':
                        if response.get('refund_status') == 'REFUND_SUCCESS':
                            if status != '5':
                                order.status = '5'
                                order.save()
                                is_update = True
                    else:
                        failure_list.append(f'订单{order_no}接口返回错误，{response}')
                else:
                    failure_list.append(f'订单{order_no}接口返回错误，{response}')
            elif code == '20000':
                failure_list.append(f'订单{order_no}接口返回错误，{response}')
            elif code == '40004':
                if status != '1':
                    order.status = '1'
                    order.save()
                    is_update = True
            else:
                failure_list.append(f'订单{order_no}接口返回错误，{response}')
            if is_update:
                logger.info(f'订单{order_no}状态已由 {status_display} 更新为 {order.get_status_display()}')
                update_list.append(f'订单{order_no}状态已由 {status_display} 更新为 {order.get_status_display()}')
            else:
                not_update_list.append(f'订单{order_no}状态未更新')
        if len(update_list) > 0:
            message_success = ','.join(update_list)
            self.message_user(request, message_success)
        if len(not_update_list) == order_num:
            self.message_user(request, f'{order_num}个订单检查完毕，没有订单需要更新')
        if len(failure_list) > 0:
            message_failure = ','.join(failure_list)
            self.message_user(request, message_failure, level=messages.ERROR)


    make_check_status.short_description = '对 %(verbose_name_plural)s 状态进行核查'

    # 标记为发布状态的actions
    def make_refund(self, request, queryset):
        print(request)
        print(queryset.all())
        verbose_name_plural = getattr(self.model._meta, 'verbose_name_plural', self.model._meta.model_name)
        success_list = []
        failure_list = []
        refunded_list = []
        for order in queryset:
            print('order:',order)
            order_no = order.order_no
            trade_no = order.trade_no
            print(order_no)
            if order.status == '2':
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
                response = alipay.api_alipay_trade_refund(str(order.total_price), out_trade_no=order_no, trade_no=trade_no)
                if response.get('code') == '10000':
                    order.status = '5'
                    order.save()
                    success_list.append(order_no)
                else:
                    failure_list.append(order_no)
        message_success = "{0}个{1} 成功进行退款.{2}".format(len(success_list), verbose_name_plural, ','.join(success_list))
        self.message_user(request, message_success)
        if len(failure_list) > 0:
            message_failure = "{0}个{1} 退款失败.{2}".format(len(failure_list), verbose_name_plural, ','.join(failure_list))
            self.message_user(request, message_failure, level=messages.ERROR)

    make_refund.short_description = '对 %(verbose_name_plural)s 进行退款'

    def review_status(self, obj):
        return format_html(f'''
        <a href="javascript:void(0)" onclick="review_status('{obj.order_no}')">核查</a>
        ''')

    review_status.type = 'success'
    review_status.short_description = '手动核查状态'

    def order_refund(self, obj):
        if obj.status == '2':
            return format_html(f'''
            <a href="javascript:void(0)" onclick="order_refund('{obj.order_no}', '{obj.total_price}')">退款</a>
            ''')
        else:
            return ''

    order_refund.type = 'success'
    order_refund.short_description = '操作'

    # actions = ['delete_selected']
    #
    # def delete_selected(self, request, queryset):
    #     queryset.update(is_delete=True)
    #
    # delete_selected.short_description = '删除所选项'

    class Media:
        js = ('app/js/jquery-3.6.1.min.js', 'app/lib/layer/layer.js', 'order/js/job_run.js')



class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'password']
    list_display_links = ('name',)

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_no', 'reason', 'email', 'alipay_no','content']
    list_display_links = ('order_no',)


admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Post, PostAdmin)
