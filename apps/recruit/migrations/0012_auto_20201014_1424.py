# Generated by Django 2.0.13 on 2020-10-14 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0011_auto_20201013_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=50)),
                ('file', models.FileField(blank=True, null=True, unique=True, upload_to='excel_data')),
            ],
            options={
                'verbose_name': '批量添加试题',
                'verbose_name_plural': '批量添加试题',
            },
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_choice',
            field=models.TextField(blank=True, null=True, verbose_name='选择题答案'),
        ),
    ]