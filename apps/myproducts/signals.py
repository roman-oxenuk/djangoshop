# coding: utf-8
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import post_delete

from mydiscounts.models import (
    SingleItemDiscount,
    BrandDiscount,
    CategoryDiscount,
)


@receiver(post_save, sender=SingleItemDiscount)
@receiver(post_delete, sender=SingleItemDiscount)
def recalculate_discounted_price_by_single_discount(sender, instance, **kwargs):
    instance.for_item.save()


@receiver(post_save, sender=BrandDiscount)
@receiver(post_delete, sender=BrandDiscount)
def recalculate_discounted_price_by_brand_discount(sender, instance, **kwargs):
    brand_products = instance.for_brand.myproduct_set.all()
    for product in brand_products:
        product.save()


@receiver(post_save, sender=CategoryDiscount)
@receiver(post_delete, sender=CategoryDiscount)
def recalculate_discounted_price_by_category_discount(sender, instance, **kwargs):
    category_products = instance.for_category.myproduct_set.all()
    for product in category_products:
        product.save()
