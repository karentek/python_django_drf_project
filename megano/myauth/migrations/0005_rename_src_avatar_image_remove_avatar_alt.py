# Generated by Django 4.2.6 on 2023-11-05 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0004_rename_avatar_avatar_src_avatar_alt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='avatar',
            old_name='src',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='avatar',
            name='alt',
        ),
    ]
