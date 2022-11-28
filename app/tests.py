# -*- coding: utf-8 -*-
import os,django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','firm.settings')
django.setup()

from app.models import CaseType,Case,Customer


type_list = CaseType.objects.all().prefetch_related('case_set')
# case_list = Case.objects.all().select_related('type')
# print(case_list.values())
# print(case_list[0].type)
# print(type_list)
# for d in type_list:
#     print(d.case_set.all())

# c2=Case.objects.filter(id__gt=3, published=True).order_by('id')
# c=Case.objects.all().values('id','title')
# c1=Case.objects.filter(id=4, published=True).order_by('id')
# print(c)
# print(c1)
# print(c2)

t1 = CaseType.objects.all()[2]
t=t1.case_set()
print(t)
for i in t:
    print(i)
