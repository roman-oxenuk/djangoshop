from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from polymorphic.polymorphic_model import (
        PolymorphicModel,
        PolymorphicModelBase,
        )

from shop.util.loader import get_model_string
from shop.cart.cart_modifiers_base import BaseCartModifier

from .managers import DiscountBaseManager


class DiscountMetaclass(PolymorphicModelBase):
    def __new__(cls, name, bases, attrs):
        attrs['product_filters'] = []
        return super(DiscountMetaclass, cls).__new__(cls, name, bases, attrs)


class DiscountBase(PolymorphicModel, BaseCartModifier):
    """
    Base discount model.
    """
    __metaclass__ = DiscountMetaclass

    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=30,
            blank=True, null=False,
            help_text=_('Is discount valid only with included code'))

    is_active = models.BooleanField(_('Is active'), default=True)
    valid_from = models.DateTimeField(_('Valid from'), default=datetime.now)
    valid_until = models.DateTimeField(_('Valid until'), blank=True, null=True)

    num_uses = models.IntegerField(_('Number of times already used'),
            default=0)

    objects = DiscountBaseManager()

    def __init__(self, *args, **kwargs):
        self._eligible_products_cache = {}
        return super(DiscountBase, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')
        ordering = []

    def __unicode__(self):
        return self.get_name()

    def get_name(self):
        return self.name

    @classmethod
    def register_product_filter(cls, filt):
        """
        Register filters that affects which products this discount class
        may apply to.
        """
        cls.product_filters.append(filt)

    def get_products(self):
        """
        Return initial product queryset of products eligible for discount.

        Default implementation returns al products.

        Subclasses can override this method to filter products further,
        ie by category or exclude products that are on sale.
        """
        product_class_string = settings.get('SHOP_PRODUCT_MODEL')
        product_class = __import__(product_class_string)
        return product_class.objects.all()

    def eligible_products(self, in_products=None):
       """
       Returns queryset of products that discount may apply to.

       1. get initial initial product queryset with ``get_products``

       2. apply each of product filters registered with
          ``register_product_filter``

       3. intersect queryset with ``in_products`` products, if ``in_products``
          is given
       """
       cache_key = tuple(in_products) if in_products else None
       try:
           qs = self._eligible_products_cache[cache_key]
       except KeyError:
           qs = self.get_products()
           for filt in self.__class__.product_filters:
               if callable(filt):
                   qs = filt(self, qs)
               elif type(filt) is dict:
                   qs = qs.filter(**filt)
               else:
                   qs = qs.filter(filt)
           if in_products:
               qs = qs.filter(id__in=[p.id for p in in_products])
           qs = qs.distinct()
           self._eligible_products_cache[cache_key] = qs
       return qs

    def is_eligible_product(self, product, cart):
        """
        Returns if given product in cart should be discounted.
        """
        products = set([cart_item.product for cart_item in cart.items.all()])
        eligible_products_in_cart = self.eligible_products(products)
        return product in eligible_products_in_cart


class CartDiscountCode(models.Model):
    """
    Model holds entered discount code for ``Cart``.
    """
    cart = models.ForeignKey(get_model_string('Cart'), editable=False)
    code = models.CharField(_('Discount code'), max_length=30)

    class Meta:
        verbose_name = _('Cart discount code')
        verbose_name_plural = _('Cart discount codes')

    def clean_fields(self, *args, **kwargs):
        super(CartDiscountCode, self).clean_fields(*args, **kwargs)
        if not DiscountBase.objects.active(code=self.code):
            msg = _('Discount code is invalid or expired.')
            raise ValidationError({'code': [msg]})
