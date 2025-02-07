# Generated by Django 4.0 on 2022-04-06 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('krishibariapp', '0025_alter_courseslist_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseslist',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='krishibariapp.dbtable'),
        ),
        migrations.AddField(
            model_name='dbtable',
            name='profile_pic',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
    ]
