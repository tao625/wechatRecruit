# Generated by Django 2.2.11 on 2020-09-28 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0003_auto_20200928_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='name',
            field=models.CharField(max_length=100, verbose_name='性格别名'),
        ),
    ]
