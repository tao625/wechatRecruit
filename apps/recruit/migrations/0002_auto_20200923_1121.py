# Generated by Django 2.2.11 on 2020-09-23 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='options',
            name='questionId',
        ),
        migrations.AddField(
            model_name='options',
            name='questionId',
            field=models.ManyToManyField(to='recruit.Question', verbose_name='关联题目'),
        ),
    ]
