from django.contrib import admin
from order.models import Goods, OrderInfo


# Register your models here.
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'email']
    list_display_links = ('order_no',)


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'password']
    list_display_links = ('name',)


admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register(Goods, GoodsAdmin)
