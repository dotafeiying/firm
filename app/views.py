from django.shortcuts import render,redirect,reverse
from .models import Case,CaseType,Customer,CustomerType,About

# Create your views here.

def index(request):
    # return render(request,'app/home.html')
    return redirect(reverse('app:home'))

def home(request):
    # return redirect(reverse('app:index'))
    return render(request, 'app/home.html')

def about(request):
    context={}
    about_list=About.objects.filter(is_show=True)
    context['about_list']=about_list
    return render(request,'app/about.html',context)

def case(request):
    context = {}
    type_list = CaseType.objects.all()
    case_list = Case.published.all()
    hot_case_list = Case.published.filter(is_hot=True)
    print(type_list)
    context['type_list'] = type_list
    context['case_list'] = case_list
    context['hot_case_list'] = hot_case_list
    return render(request,'app/case.html',context)

def customer(request):
    context = {}
    type_list = CustomerType.objects.all()
    customer_list = Customer.published.all()
    print(type_list)
    context['type_list'] = type_list
    context['customer_list'] = customer_list
    return render(request,'app/customer.html',context)

def case_detail(request,case_slug):
    print(case_slug)
    context={}
    case = Case.objects.get(slug=case_slug)
    case.views += 1
    case.save(update_fields=['views'])
    context['case'] = case
    return render(request,'app/case_detail.html',context)

def customer_detail(request,customer_slug):
    print(customer_slug)
    context={}
    customer = Customer.objects.get(slug=customer_slug)
    customer.views += 1
    customer.save(update_fields=['views'])
    context['customer'] = customer
    return render(request,'app/customer_detail.html',context)
