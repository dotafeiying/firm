from django.forms import ModelForm, TextInput,ChoiceField, Form,Textarea,CharField,EmailInput
from django.utils.translation import gettext_lazy as _
from .models import OrderInfo, Goods, Post
from django.core.exceptions import ValidationError



class OrderInfoForm(ModelForm):
    class Meta:
        model = OrderInfo
        fields = '__all__'

class OrderCreateForm(ModelForm):
    class Meta:
        model = OrderInfo
        fields = ['total_count', 'pay_method', 'email']
        help_texts = {
            'email': _('请输入常用邮箱'),
        }
        widgets = {
            'email': TextInput(
                attrs={
                    "type": "email",
                    "placeholder": _("E-mail address"),
                    "autocomplete": "email",
                }
            )
        }

class PostForm(ModelForm):
    # order_no = CharField(max_length=30, label='订单号', required=True)
    class Meta:
        model = Post
        fields = ['order_no', 'reason', 'email','alipay_no','content']
        help_texts = {
            'email': _('请输入常用邮箱'),
        }
        widgets = {
            'order_no': TextInput(attrs={'placeholder': '请填写需要投诉的订单编号'}),
            # 'reason': TextInput(attrs={'placeholder': 'test'}),
            'email': EmailInput(attrs={'placeholder': '用于卖家跟你联系和沟通'}),
            # 'email': TextInput(attrs={"type": "email", 'placeholder': '用于卖家跟你联系和沟通', "autocomplete": "email"}),
            'alipay_no': TextInput(attrs={'placeholder': '用于平台购买款项退回，请务必真实填写。'}),
            'content': Textarea(attrs={'placeholder': '这里描述你的具体问题以及诉求'}),
        }

    def clean_order_no(self):
        order_no = self.cleaned_data.get('order_no')
        order = OrderInfo.objects.filter(order_no=order_no).first()
        if order is None:
            raise ValidationError('订单编号不存在')
        else:
            return order_no

