# Generated by Django 4.1.7 on 2023-06-29 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='uuid',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, unique=True),
        ),
    ]