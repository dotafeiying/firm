from import_export import resources
from .models import Case,Customer

class CaseResource(resources.ModelResource):

    class Meta:
        model = Case
        # exclude = ('id',)
        # fields = ('id', 'title','slug','img','abstract','type','views','content', 'is_hot')

class CustomerResource(resources.ModelResource):

    class Meta:
        model = Customer