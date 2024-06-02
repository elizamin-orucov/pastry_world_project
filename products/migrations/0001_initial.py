# Generated by Django 4.2 on 2024-05-31 12:22

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import services.uploader


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=70)),
                ('icon', models.ImageField(blank=True, null=True, upload_to=services.uploader.Uploader.category_logo_uploader)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('code', models.SlugField(editable=False, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('description', ckeditor.fields.RichTextField()),
                ('price', models.FloatField()),
                ('status', models.CharField(choices=[('Sold', 'Sold'), ('In stock', 'In stock'), ('Will available', 'Will available')], max_length=50)),
                ('discount_interest', models.IntegerField(blank=True, choices=[(5, '5% off'), (10, '10% off'), (15, '15% off'), (20, '20% off'), (25, '25% off'), (30, '30% off'), (40, '40% off'), (50, '50% off'), (60, '60% off'), (70, '70% off')], null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to=services.uploader.Uploader.product_image_uploader)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'Product images',
            },
        ),
    ]
