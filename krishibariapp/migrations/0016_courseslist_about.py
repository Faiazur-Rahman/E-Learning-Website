# Generated by Django 4.0 on 2022-03-29 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krishibariapp', '0015_allblogs_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseslist',
            name='about',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
