# Generated by Django 4.1.5 on 2023-02-19 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_rename_yt_video_videos'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Videos',
            new_name='Video',
        ),
    ]