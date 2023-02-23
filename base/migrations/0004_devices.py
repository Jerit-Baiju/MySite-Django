# Generated by Django 4.1.5 on 2023-02-23 14:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0003_rename_videos_video"),
    ]

    operations = [
        migrations.CreateModel(
            name="Devices",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.CharField(max_length=225, null=True)),
                ("user_id", models.IntegerField()),
            ],
        ),
    ]