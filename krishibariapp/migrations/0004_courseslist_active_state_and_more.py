# Generated by Django 4.0 on 2022-02-13 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krishibariapp', '0003_courseslist_strawbarryvideotable_allcoursevideos'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseslist',
            name='active_state',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='courseslist',
            name='course_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]