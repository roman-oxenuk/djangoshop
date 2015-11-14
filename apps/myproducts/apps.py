# coding: utf-8
from django.apps import AppConfig


class MyProductsConfig(AppConfig):

    name = u'myproducts'
    verbose_name = u'Товары'

    def ready(self):
        import myproducts.signals