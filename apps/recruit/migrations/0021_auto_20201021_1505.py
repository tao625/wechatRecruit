# Generated by Django 2.0.13 on 2020-10-21 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0020_auto_20201019_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='respondenttoken',
            name='id',
        ),
        migrations.AlterField(
            model_name='respondenttoken',
            name='key',
            field=models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='key'),
        ),
    ]
