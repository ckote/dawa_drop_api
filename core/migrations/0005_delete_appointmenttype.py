# Generated by Django 4.1.7 on 2023-06-15 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_patientnextofkeen_email_delete_appointment'),
        ('core', '0004_notification'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AppointMentType',
        ),
    ]
