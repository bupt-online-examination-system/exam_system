# Generated by Django 2.2 on 2019-04-11 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='start_time',
            field=models.DateTimeField(default='1970-01-01 00:00:00'),
        ),
    ]
