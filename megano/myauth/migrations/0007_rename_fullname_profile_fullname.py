# Generated by Django 4.2.6 on 2023-11-09 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0006_remove_avatar_user_profile_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='fullname',
            new_name='fullName',
        ),
    ]
