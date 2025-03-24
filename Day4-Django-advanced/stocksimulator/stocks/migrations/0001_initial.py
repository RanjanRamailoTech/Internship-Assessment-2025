# Generated by Django 5.1.7 on 2025-03-21 05:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StockPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sequence', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.company')),
            ],
            options={
                'unique_together': {('company', 'sequence')},
            },
        ),
    ]
