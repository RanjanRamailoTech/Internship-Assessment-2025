# Generated by Django 5.2.1 on 2025-05-14 04:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('birth_year', models.IntegerField()),
            ],
            options={
                'indexes': [models.Index(fields=['birth_year'], name='library_aut_birth_y_9dbea1_idx')],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'indexes': [models.Index(fields=['name'], name='library_cat_name_9e55d3_idx')],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('website', models.URLField(blank=True)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='library.author')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('published_on', models.DateField()),
                ('is_modern', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='library.author')),
                ('categories', models.ManyToManyField(blank=True, related_name='books', to='library.category')),
            ],
            options={
                'indexes': [models.Index(fields=['published_on'], name='library_boo_publish_66bba3_idx'), models.Index(fields=['title'], name='library_boo_title_c38ef2_idx')],
            },
        ),
    ]
