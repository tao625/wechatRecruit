# Generated by Django 2.2.11 on 2020-09-23 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0010_auto_20200923_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='animal',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recruit.Animal'),
        ),
    ]