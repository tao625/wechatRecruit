# Generated by Django 2.0.13 on 2020-10-25 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0002_auto_20201025_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='animal',
            field=models.CharField(blank=True, help_text='仅PDP性格测试需要选择', max_length=200, null=True, verbose_name='类型别名'),
        ),
    ]
