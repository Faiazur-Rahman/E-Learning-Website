# Generated by Django 4.0 on 2022-03-20 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krishibariapp', '0013_alter_allblogs_dislikes_alter_allblogs_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allblogs',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
