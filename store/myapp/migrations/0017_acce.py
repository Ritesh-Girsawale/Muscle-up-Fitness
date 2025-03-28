# Generated by Django 5.1.4 on 2025-01-17 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_rename_pimage_view1_rimage_rename_pname_view1_rname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=50, verbose_name='Product Name')),
                ('price', models.FloatField()),
                ('category', models.IntegerField(choices=[(1, 'Shaker'), (2, 'Sandbag'), (3, 'Weightlifting Belt'), (4, 'Hand-Glooves')], verbose_name='Category')),
                ('description', models.CharField(max_length=300, verbose_name='Details')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is_Available')),
                ('pimage', models.ImageField(upload_to='image')),
            ],
        ),
    ]
