# Generated by Django 4.1.7 on 2023-06-29 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0010_alter_patient_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='national_id',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]