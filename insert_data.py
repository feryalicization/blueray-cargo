# insert_data.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shipping_project.settings")  # Replace "your_project" with your actual project name
django.setup()

from shipping.models import Country, Category

# Insert data for countries
china = Country.objects.create(country_name='China', country_flag='https://example.com/china-flag.png', country_currency='CHY')
thailand = Country.objects.create(country_name='Thailand', country_flag='https://example.com/thailand-flag.png', country_currency='THB')
singapore = Country.objects.create(country_name='Singapore', country_flag='https://example.com/singapore-flag.png', country_currency='SGD')

# Insert data for categories
Category.objects.create(country=china, category_title='Electronic', price_per_kilo=250000)
Category.objects.create(country=china, category_title='Chip', price_per_kilo=300000)
Category.objects.create(country=china, category_title='Laptop and Computer', price_per_kilo=220000)

Category.objects.create(country=thailand, category_title='Garments', price_per_kilo=200000)

Category.objects.create(country=singapore, category_title='Spare parts', price_per_kilo=210000)
