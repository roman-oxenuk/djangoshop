# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myproducts', '0005_auto_20151113_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myproduct',
            name='category',
            field=models.ManyToManyField(to=b'myproducts.Category', null=True, verbose_name='\u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', blank=True),
        ),
    ]
