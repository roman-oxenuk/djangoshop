# coding: utf-8
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):

    @property
    def personal_discounts(self):
        return self.personaldiscount_set.active()

    @property
    def personal_discount(self):
        return self.personaldiscount_set.active().order_by('-amount').first()
