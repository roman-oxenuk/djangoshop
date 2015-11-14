# coding: utf-8
from django.db import models

from discount.models import DiscountBase


class PersonalDiscount(DiscountBase):

    for_user = models.ForeignKey('myusers.MyUser', verbose_name=u'Для пользователя')
    amount = models.DecimalField(u'сумма скидки в процентах', max_digits=5, decimal_places=2)

    def get_extra_cart_price_field(self, cart, request=None):
        personal_discount = request.user.personal_discount
        if personal_discount and personal_discount == self:
            return (self.get_name(), self.calculate_discount(cart.subtotal_price),)

    def calculate_discount(self, price):
        return (self.amount * -1/100) * price

    class Meta:
        app_label = 'discount'
        verbose_name = u'Персональная скидка'
        verbose_name_plural = u'Персональные скидки'

    def get_name(self):
        return u'%s для %s (%s%%)' % (
            self._meta.verbose_name, self.for_user.username, str(self.amount))

    def __unicode__(self):
        return self.get_name()


class SingleItemDiscount(DiscountBase):

    for_item = models.ForeignKey('myproducts.MyProduct', verbose_name=u'Для товара')
    amount = models.DecimalField(u'сумма скидки в процентах', max_digits=5, decimal_places=2)

    def get_extra_cart_item_price_field(self, cart_item, request=None):
        max_discount = self.for_item.get_max_discount()
        if max_discount == self and cart_item.product == self.for_item:
            return (self.get_name(),
                    self.calculate_discount(cart_item.line_subtotal))

    def calculate_discount(self, price):
        return (self.amount * -1/100) * price

    def get_name(self):
        return u'%s %s (%s%%)' % (
            self._meta.verbose_name, self.for_item.name, str(self.amount))

    class Meta:
        app_label = 'discount'
        verbose_name = u'Скидка на товар'
        verbose_name_plural = u'Скидки на товар'

    def __unicode__(self):
        return self.get_name()


class BrandDiscount(DiscountBase):

    for_brand = models.ForeignKey('myproducts.ProductBrand', verbose_name=u'Для бренда')
    amount = models.DecimalField(u'сумма скидки в процентах', max_digits=5, decimal_places=2)

    def get_extra_cart_item_price_field(self, cart_item, request=None):
        if (cart_item.product.get_max_discount() == self and
            cart_item.product.brand == self.for_brand):
            return (self.get_name(),
                    self.calculate_discount(cart_item.line_subtotal))

    def calculate_discount(self, price):
        return (self.amount * -1/100) * price

    def get_name(self):
        return u'%s %s (%s%%)' % (
            self._meta.verbose_name, self.for_brand.name, str(self.amount))

    class Meta:
        app_label = 'discount'
        verbose_name = u'Скидка на бренд'
        verbose_name_plural = u'Скидки на бренды'

    def __unicode__(self):
        return self.get_name()


class CategoryDiscount(DiscountBase):

    for_category = models.ForeignKey('myproducts.Category', verbose_name=u'Для категории')
    amount = models.DecimalField(u'сумма скидки в процентах', max_digits=5, decimal_places=2)

    def get_extra_cart_item_price_field(self, cart_item, request=None):
        if (cart_item.product.get_max_discount() == self and
            self.for_category in cart_item.product.category.all()):
            return (self.get_name(),
                    self.calculate_discount(cart_item.line_subtotal))

    def calculate_discount(self, price):
        return (self.amount * -1/100) * price

    def get_name(self):
        return u'%s %s (%s%%)' % (
            self._meta.verbose_name, self.for_category.name, str(self.amount))

    class Meta:
        app_label = 'discount'
        verbose_name = u'Скидка на категорию'
        verbose_name_plural = u'Скидки на категории'

    def __unicode__(self):
        return self.get_name()
