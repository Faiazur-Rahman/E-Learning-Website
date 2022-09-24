# Generated by Django 4.0 on 2022-06-03 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krishibariapp', '0030_course_exam_course_exam_result_course_exam_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_exam_answer',
            name='correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='course_exam',
            name='difficulty',
            field=models.CharField(choices=[('hard', 'hard'), ('easy', 'easy'), ('medium', 'medium')], max_length=6),
        ),
    ]