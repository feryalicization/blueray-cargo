
from django.db import models

class Country(models.Model):
    country_name = models.CharField(max_length=255)
    country_flag = models.URLField()
    country_currency = models.CharField(max_length=10)

    def __str__(self):
        return self.country_name
    


class Category(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    category_title = models.CharField(max_length=255)
    price_per_kilo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.category_title
    


class Destination(models.Model):
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.city
