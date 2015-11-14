# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import shop.util.fields


class Migration(migrations.Migration):

    dependencies = [
        ('myproducts', '0002_auto_20151112_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='myproduct',
            name='discounted_price',
            field=shop.util.fields.CurrencyField(default=Decimal('0.0'), verbose_name='\u0426\u0435\u043d\u0430 \u0441 \u0443\u0447\u0451\u0442\u043e\u043c \u0441\u043a\u0438\u0434\u043a\u0438', max_digits=30, decimal_places=2),
            preserve_default=True,
        ),
    ]
