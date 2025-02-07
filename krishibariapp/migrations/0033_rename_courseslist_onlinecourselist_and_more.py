# Generated by Django 4.0 on 2022-06-13 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('krishibariapp', '0032_alter_course_exam_difficulty_alter_courseslist_about_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='coursesList',
            new_name='onlineCourseList',
        ),
        migrations.RenameModel(
            old_name='courseStudents',
            new_name='onlineCourseStudents',
        ),
        migrations.AlterField(
            model_name='course_exam',
            name='difficulty',
            field=models.CharField(choices=[('medium', 'medium'), ('easy', 'easy'), ('hard', 'hard')], max_length=6),
        ),
        migrations.CreateModel(
            name='liveCourseStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transection_id', models.TextField(blank=True, max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='krishibariapp.livecourselist')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='krishibariapp.dbtable')),
            ],
        ),
    ]
