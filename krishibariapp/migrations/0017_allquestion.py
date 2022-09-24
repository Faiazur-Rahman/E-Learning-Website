# Generated by Django 4.0 on 2022-04-01 12:03

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('krishibariapp', '0016_courseslist_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='allquestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('question', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('auther', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='krishibariapp.dbtable')),
            ],
        ),
    ]
