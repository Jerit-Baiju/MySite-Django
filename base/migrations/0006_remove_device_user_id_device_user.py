# Generated by Django 4.1.5 on 2023-02-23 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0005_rename_devices_device"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="device",
            name="user_id",
        ),
        migrations.AddField(
            model_name="device",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]