# Generated by Django 5.1.4 on 2025-01-26 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_address_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pimage1',
            field=models.ImageField(default='default.jpg', upload_to='image'),
        ),
        migrations.AddField(
            model_name='product',
            name='pimage2',
            field=models.ImageField(default='default.jpg', upload_to='image'),
        ),
        migrations.AddField(
            model_name='product',
            name='price1',
            field=models.FloatField(default=0.0),
        ),
    ]
