# Generated by Django 5.1.4 on 2025-01-16 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_view1_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='view1',
            name='category',
            field=models.IntegerField(choices=[(1, ' Protein'), (2, 'Gainer'), (3, 'Creatine'), (4, 'BCAA'), (5, 'EAA'), (6, 'Fish Oil'), (7, 'Pre-workout'), (8, 'Peanut Butter'), (9, 'Oats'), (10, 'Muesli')], verbose_name='Category'),
        ),
    ]
