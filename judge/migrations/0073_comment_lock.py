# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-13 08:08
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0072_contest_logo_override_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentLock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(db_index=True, max_length=30, validators=[django.core.validators.RegexValidator(b'^[pc]:[a-z0-9]+$|^b:\\d+$|^s:', 'Page code must be ^[pc]:[a-z0-9]+$|^b:\\d+$')], verbose_name='associated Page')),
            ],
            options={
                'permissions': (('override_comment_lock', 'Override comment lock'),),
            },
        ),
        migrations.AlterField(
            model_name='problem',
            name='organizations',
            field=models.ManyToManyField(blank=True, help_text='If private, only these organizations may see the problem.', to='judge.Organization', verbose_name='organizations'),
        ),
    ]
