# Generated by Django 2.1 on 2018-10-11 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20181011_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentrecordworkshop',
            name='paid',
            field=models.IntegerField(default=0),
        ),
    ]
