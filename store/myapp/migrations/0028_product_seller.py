# Generated by Django 5.1.4 on 2025-02-20 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0027_alter_bmirecord_height'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.CharField(default='Default Name', max_length=50, verbose_name='seller'),
        ),
    ]
