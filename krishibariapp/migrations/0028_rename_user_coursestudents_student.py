# Generated by Django 4.0 on 2022-05-18 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('krishibariapp', '0027_alter_allcoursevideos_caption_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursestudents',
            old_name='user',
            new_name='student',
        ),
    ]
