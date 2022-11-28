# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-15 17:20
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='标题')),
                ('abstract', models.CharField(blank=True, help_text='可选项，若为空格则摘取正文钱54个字符', max_length=54, null=True, verbose_name='摘要')),
                ('img', models.ImageField(upload_to='pictures/case/%Y/%m/%d', verbose_name='展示图片')),
                ('slug', models.CharField(max_length=256, unique=True, verbose_name='网址')),
                ('content', DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='内容')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='浏览量')),
                ('published', models.BooleanField(default=True, verbose_name='正式发布')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name_plural': '成功案例',
                'verbose_name': '成功案例',
            },
        ),
        migrations.CreateModel(
            name='CaseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='案例类别名字')),
                ('slug', models.CharField(db_index=True, max_length=256, verbose_name='案例类别网址')),
                ('intro', models.TextField(default='', verbose_name='案例类别简介')),
                ('nav_display', models.BooleanField(default=True, verbose_name='导航显示')),
                ('home_display', models.BooleanField(default=True, verbose_name='首页显示')),
            ],
            options={
                'verbose_name_plural': '案例类别',
                'ordering': ['name'],
                'verbose_name': '案例类别',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='标题')),
                ('img', models.ImageField(upload_to='pictures/customer/%Y/%m/%d', verbose_name='展示图片')),
                ('slug', models.CharField(max_length=256, unique=True, verbose_name='网址')),
                ('content', DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='内容')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='浏览量')),
                ('published', models.BooleanField(default=True, verbose_name='正式发布')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name_plural': '行业客户',
                'verbose_name': '行业客户',
            },
        ),
        migrations.CreateModel(
            name='CustomerType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='客户类别名字')),
                ('slug', models.CharField(db_index=True, max_length=256, verbose_name='客户类别网址')),
                ('intro', models.TextField(default='', verbose_name='客户类别简介')),
                ('nav_display', models.BooleanField(default=True, verbose_name='导航显示')),
                ('home_display', models.BooleanField(default=True, verbose_name='首页显示')),
            ],
            options={
                'verbose_name_plural': '客户类别',
                'ordering': ['name'],
                'verbose_name': '客户类别',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='column',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.CustomerType', verbose_name='案例类别'),
        ),
        migrations.AddField(
            model_name='case',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.CaseType', verbose_name='案例类别'),
        ),
    ]