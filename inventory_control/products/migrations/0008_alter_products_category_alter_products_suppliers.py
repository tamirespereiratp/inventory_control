# Generated by Django 5.0.2 on 2024-02-22 01:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_category_slug_supplierproduct_and_more'),
        ('suppliers', '0002_alter_suppliers_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category'),
        ),
        migrations.AlterField(
            model_name='products',
            name='suppliers',
            field=models.ManyToManyField(blank=True, through='products.SupplierProduct', to='suppliers.suppliers'),
        ),
    ]
