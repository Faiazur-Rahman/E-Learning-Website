# Generated by Django 4.0 on 2022-04-01 17:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('krishibariapp', '0017_allquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='allquestion',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
