# Generated by Django 3.1.2 on 2020-12-23 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20201223_1932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='views',
        ),
        migrations.AddField(
            model_name='post',
            name='hits',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
