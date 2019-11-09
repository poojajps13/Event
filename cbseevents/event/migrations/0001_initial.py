# Generated by Django 2.2.7 on 2019-11-09 14:39

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=50)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EventRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('type', models.CharField(max_length=50)),
                ('c_o_e', models.CharField(max_length=75)),
                ('event_name', models.CharField(max_length=110)),
                ('event_pic', models.FileField(default='', upload_to='')),
                ('fees', models.FloatField()),
                ('registration_start', models.DateField()),
                ('registration_end', models.DateField()),
                ('event_date', models.DateField()),
                ('duration_number', models.CharField(max_length=10)),
                ('duration_string', models.CharField(max_length=10)),
                ('eligible_branches', models.CharField(max_length=100)),
                ('eligible_year', models.CharField(max_length=100)),
                ('pre_requisites_1', models.CharField(default='', max_length=50)),
                ('pre_requisites_2', models.CharField(default='', max_length=50)),
                ('pre_requisites_3', models.CharField(default='', max_length=50)),
                ('learning_outcome_1', models.CharField(default='', max_length=100)),
                ('learning_outcome_2', models.CharField(default='', max_length=100)),
                ('learning_outcome_3', models.CharField(default='', max_length=100)),
                ('learning_outcome_4', models.CharField(default='', max_length=100)),
                ('learning_outcome_5', models.CharField(default='', max_length=100)),
                ('learning_outcome_6', models.CharField(default='', max_length=100)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('outside_student', models.IntegerField(default=0)),
                ('venue', models.CharField(max_length=50)),
                ('resource_person', models.CharField(max_length=110)),
                ('resource_person_pic', models.FileField(default='', upload_to='')),
                ('resource_person_data', ckeditor_uploader.fields.RichTextUploadingField()),
                ('registered_student', models.IntegerField(default=0)),
                ('registration_open', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
