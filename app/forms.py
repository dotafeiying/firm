from django.forms import ModelForm
from .widgets import IconWidget
from.models import About
class AboutForm(ModelForm):
    class Meta:
        model = About
        fields = '__all__'
        widgets = {
            'img': IconWidget(attrs={'cols': '100', 'rows': '20'}),
        }
