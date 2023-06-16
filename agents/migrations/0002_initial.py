# Generated by Django 4.1.7 on 2023-05-16 08:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agents', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveragent',
            name='delivery_mode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agents', to='core.deliverymode'),
        ),
        migrations.AddField(
            model_name='deliveragent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='deliveragent',
            name='work_clinic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agents', to='core.healthfacility'),
        ),
    ]