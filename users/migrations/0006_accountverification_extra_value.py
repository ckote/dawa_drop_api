# Generated by Django 4.1.7 on 2023-07-05 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_accountverification_extra_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountverification',
            name='extra_value',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
