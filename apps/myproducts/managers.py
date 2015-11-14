from django.db.models import Prefetch

from shop.models_bases.managers import ProductManager


class MyProductManager(ProductManager):

    def get_query_set(self):
        qs = super(ProductManager, self).get_query_set()

        qs = qs.select_related('brand')
        brand_perf = Prefetch('brand__branddiscount_set', to_attr='brand_discounts')
        qs = qs.prefetch_related(brand_perf)

        qs = qs.prefetch_related('category')
        category_pref = Prefetch('category__categorydiscount_set', to_attr='category_discounts')
        qs = qs.prefetch_related(category_pref)

        single_discounts_pref = Prefetch('singleitemdiscount_set', to_attr='single_discounts')
        qs = qs.prefetch_related(single_discounts_pref)

        return qs
