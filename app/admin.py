# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import Case,CaseType,Customer,CustomerType,About,Settings,SettingsGroup,Notification
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from .resources import CaseResource,CustomerResource
from .forms import AboutForm

# Register your models here.

# admin.site.site_header = '软诚技术管理系统'
admin.site.site_title = '软诚技术'


class BaseAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    actions = ['make_published']

    # 标记为发布状态的actions
    def make_published(self, request, queryset):
        print(queryset)
        verbose_name_plural = getattr(self.model._meta,'verbose_name_plural',self.model._meta.model_name)
        rows_updated = queryset.update(is_publish=True)
        message_bit = "{0}个{1} 成功标记为发布状态.".format(rows_updated, verbose_name_plural)
        self.message_user(request, message_bit)
    make_published.short_description = '标记 %(verbose_name_plural)s 为发布状态'

class CaseAdmin(BaseAdmin):
    list_per_page = 50
    list_display = ['id', 'title','views','get_absolute_url','is_publish','is_hot','type','pub_date', 'update_time']
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_hot']
    list_display_links = ('title',)

    resource_class = CaseResource
    # actions = [make_published]


class CustomerAdmin(BaseAdmin):
    list_per_page = 50
    list_display = ['id', 'title','slug','views','is_publish','type','pub_date', 'update_time']
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ('title',)

    resource_class = CustomerResource

class CustomerTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','intro', 'nav_display', 'home_display']
    list_display_links = ('name',)

class CaseTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','intro', 'nav_display', 'home_display']
    list_display_links = ('name',)

class AboutAdmin(admin.ModelAdmin):
    form = AboutForm
    list_display = ['name','img','is_show']
    list_display_links = ('name',)

class SettingsInline(admin.TabularInline):
    model = Settings
    # readonly_fields = ['title',]
    fields = [ 'title','value', 'var']
    # raw_id_fields = ['settingsgroup']
    # extra = 3  # 默认显示条目的数量
    # list_display_links = ('title',)
    readonly_fields = ['title', 'var']

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1

class SettingsGroupAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_display_links = ('name',)
    inlines = [SettingsInline, ]

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['id','action_time','user','content_type','object_repr','action_flag','change_message']
    list_display_links = ('object_repr',)

admin.site.register(LogEntry,LogEntryAdmin)

admin.site.register(Case,CaseAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(CustomerType,CustomerTypeAdmin)
admin.site.register(CaseType,CaseTypeAdmin)
admin.site.register(About,AboutAdmin)
# admin.site.register(Settings,SettingsInline)
admin.site.register(SettingsGroup,SettingsGroupAdmin)
admin.site.register(Notification)
