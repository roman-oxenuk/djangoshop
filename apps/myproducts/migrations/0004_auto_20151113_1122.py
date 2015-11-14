# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myproducts', '0003_myproduct_discounted_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0431\u0440\u0435\u043d\u0434\u0430')),
            ],
            options={
                'verbose_name': '\u0431\u0440\u0435\u043d\u0434',
                'verbose_name_plural': '\u0431\u0440\u0435\u043d\u0434\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='myproduct',
            options={'ordering': ['discounted_price'], 'verbose_name': '\u0442\u043e\u0432\u0430\u0440', 'verbose_name_plural': '\u0442\u043e\u0432\u0430\u0440\u044b'},
        ),
        migrations.AddField(
            model_name='myproduct',
            name='brand',
            field=models.ForeignKey(verbose_name='\u0431\u0440\u0435\u043d\u0434', blank=True, to='myproducts.ProductBrand', null=True),
            preserve_default=True,
        ),
    ]
