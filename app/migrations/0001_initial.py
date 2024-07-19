# Generated by Django 5.0.6 on 2024-07-18 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KaspiGoodsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=256)),
                ('model', models.CharField(max_length=256)),
                ('brand', models.CharField(max_length=256)),
                ('price', models.IntegerField()),
                ('pp1', models.CharField(max_length=256, null=True)),
                ('pp2', models.CharField(max_length=256, null=True)),
                ('pp3', models.CharField(max_length=256, null=True)),
                ('pp4', models.CharField(max_length=256, null=True)),
                ('pp5', models.CharField(max_length=256, null=True)),
                ('preorder', models.CharField(max_length=256, null=True)),
                ('competitors_prices', models.JSONField(null=True, verbose_name='Цены конкурентов')),
                ('min_price', models.IntegerField(verbose_name='Минимальная цена')),
                ('price_step', models.IntegerField(verbose_name='Шаг цены')),
            ],
            options={
                'db_table': 'kaspi_goods',
            },
        ),
    ]
