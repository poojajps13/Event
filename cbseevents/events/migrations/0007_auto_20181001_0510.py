# Generated by Django 2.1 on 2018-10-01 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_workshoprecord_registered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshoprecord',
            name='registered',
            field=models.IntegerField(default=0, editable=False, max_length=7),
        ),
    ]
