# Generated by Django 4.0 on 2022-04-06 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krishibariapp', '0024_alter_courseslist_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseslist',
            name='image',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
    ]
