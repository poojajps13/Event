# Generated by Django 2.1.1 on 2018-12-04 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_auto_20181205_0226'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventrecord',
            name='close',
            field=models.BooleanField(default=False),
        ),
    ]
