# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-22 11:15
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20180518_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu', models.IntegerField(choices=[(1, '首页'), (2, '技术服务'), (3, '行业客户'), (4, '成功案例'), (5, '升级日志'), (6, '关于软诚')], verbose_name='菜单')),
                ('image', models.ImageField(upload_to='banner', verbose_name='轮播图片')),
                ('index', models.IntegerField(default=0, verbose_name='轮播顺序')),
                ('desc1', models.CharField(blank=True, default='', help_text='可选项，最多15个字符', max_length=15, verbose_name='描述1')),
                ('desc2', models.CharField(blank=True, default='', help_text='可选项，建议不超过20个字符', max_length=20, verbose_name='描述2')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
                ('is_use', models.BooleanField(default=True, verbose_name='在用？')),
            ],
            options={
                'verbose_name': '轮播商品',
                'verbose_name_plural': '轮播商品',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='标题')),
                ('content', DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='内容')),
                ('post_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发送时间')),
            ],
        ),
        migrations.AlterField(
            model_name='settings',
            name='value',
            field=models.CharField(blank=True, max_length=256, verbose_name='变量值'),
        ),
    ]