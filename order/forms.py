from django.forms import ModelForm, TextInput,ChoiceField
from django.utils.translation import gettext_lazy as _
from .models import OrderInfo, Goods



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