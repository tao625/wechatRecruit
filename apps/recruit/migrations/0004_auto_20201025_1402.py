# Generated by Django 2.0.13 on 2020-10-25 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0003_auto_20201025_1249'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'verbose_name': '最终分析报告', 'verbose_name_plural': '最终分析报告'},
        ),
        migrations.AddField(
            model_name='report',
            name='total_scores',
            field=models.TextField(blank=True, null=True, verbose_name='得分汇总'),
        ),
        migrations.AlterField(
            model_name='character',
            name='animal',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='类型别名'),
        ),
        migrations.AlterField(
            model_name='question',
            name='must',
            field=models.BooleanField(default=True, verbose_name='是否必填'),
        ),
    ]
