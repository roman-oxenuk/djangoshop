from django.contrib import admin

from myproducts.models import (
    MyProduct,
    ProductBrand,
    Category,
)


class MyProductAdmin(admin.ModelAdmin):

    readonly_fields = ('discounted_price',)


admin.site.register(MyProduct, MyProductAdmin)
admin.site.register(ProductBrand)
admin.site.register(Category)
