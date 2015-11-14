# coding: utf-8
from django.db import models

from shop.models_bases import BaseProduct
from shop.models_bases.managers import ProductStatisticsManager
from shop.util.fields import CurrencyField

from .managers import MyProductManager


class Category(models.Model):

    name = models.CharField(u'Название категории', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'категории'


class ProductBrand(models.Model):

    name = models.CharField(u'Название бренда', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'бренд'
        verbose_name_plural = u'бренды'


class MyProduct(BaseProduct):

    brand = models.ForeignKey(ProductBrand, verbose_name=u'бренд', null=True, blank=True)
    category = models.ManyToManyField(Category, verbose_name=u'категория', null=True, blank=True)
    discounted_price = CurrencyField(verbose_name=u'Цена с учётом скидки')

    def get_max_discount(self):
        all_discounts = []
        all_discounts.extend(self.singleitemdiscount_set.all())

        if self.brand:
            all_discounts.extend(self.brand.brand_discounts)

        for cat in self.category.all():
            all_discounts.extend(cat.category_discounts)

        if all_discounts:
            return max(all_discounts, key=lambda x: x.amount)

    def recalculate_discounted_price(self):
        price = self.get_price()
        max_discount = self.get_max_discount()
        if max_discount:
            self.discounted_price = price + ((max_discount.amount * -1/100) * price)
        else:
            self.discounted_price = price

    def save(self, *args, **kwargs):
        self.recalculate_discounted_price()
        super(MyProduct, self).save(*args, **kwargs)

    objects = MyProductManager()
    statistics = ProductStatisticsManager()

    class Meta:
        verbose_name = u'товар'
        verbose_name_plural = u'товары'
        ordering = ['discounted_price']
