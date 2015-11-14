from django.contrib import admin

from .models import (
    PersonalDiscount,
    SingleItemDiscount,
    BrandDiscount,
    CategoryDiscount,
)


admin.site.register(PersonalDiscount)
admin.site.register(SingleItemDiscount)
admin.site.register(BrandDiscount)
admin.site.register(CategoryDiscount)
