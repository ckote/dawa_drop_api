# Generated by Django 4.1.7 on 2023-06-28 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0009_alter_patient_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]
