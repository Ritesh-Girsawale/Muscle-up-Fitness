# Generated by Django 5.1.4 on 2025-01-14 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=50, verbose_name='Product Name')),
                ('price', models.FloatField()),
                ('category', models.IntegerField(choices=[(1, 'Protine'), (2, 'Gainer'), (3, 'Creatine')], verbose_name='Category')),
                ('description', models.CharField(max_length=300, verbose_name='Details')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is_Available')),
                ('pimage', models.ImageField(upload_to='image')),
            ],
        ),
    ]
