# Generated by Django 5.1.4 on 2025-01-13 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.IntegerField(choices=[(1, 'Protine'), (2, 'Gainer'), (3, 'Creatine'), (4, 'Pre-workout')], verbose_name='Category'),
        ),
    ]
